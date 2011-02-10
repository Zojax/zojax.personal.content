##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, component, event
from zope.security import checkPermission
from zope.component import getUtilitiesFor, getAdapter
from zope.i18n import translate
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.proxy import removeSecurityProxy
from zope.security.interfaces import IPrincipal
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.catalog.utils import getRequest
from zojax.catalog.catalog import queryCatalog
from zojax.content.type.interfaces import IItem
from zojax.content.type.container import ContentContainer
from zojax.content.draft.container import DraftContainer
from zojax.content.draft.interfaces import IDraftContentType, IDraftContainer
from zojax.content.space.workspace import WorkspaceFactory
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.personal.space.interfaces import IPersonalWorkspaceDescription
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.security.utils import checkPermissionForPrincipal

from interfaces import _, IContentWorkspace, IContentWorkspaceFactory


class ContentWorkspace(ContentContainer):
    interface.implements(IContentWorkspace, IItem)

    title = _(u'Your stuff')

    __name__ = u'content'

    @property
    def space(self):
        return self.__parent__


class ContentSized(object):
    interface.implements(ISized)
    component.adapts(IContentWorkspace)

    def __init__(self, context):
        self.context = context
        self._size = self._getLength()

    def _getLength(self):
        principal = self.context.__parent__.principal
        types = [name for name, ct in component.getUtilitiesFor(
                IDraftContentType)]

        #latest content
        length = len(queryCatalog(
                owners = {'any_of': (principal.id,),},
                type = {'any_of': types},
                draftContent = {'any_of': (False,)})[:15])

        #draft
        length += ISized(self.context['draft']).sizeForSorting()[1]

        return length

    def sizeForSorting(self):
        return "item", self._size

    def sizeForDisplay(self):
        return byteDisplay(self._size)


class ContentWorkspaceDescription(object):
    interface.implements(IPersonalWorkspaceDescription)

    name = u'content'
    title = _(u'Your stuff')
    description = u''

    def createTemp(self, context):
        ws = ContentWorkspace()
        ws.__parent__ = context
        return ws


class ContentWorkspaceFactory(WorkspaceFactory):
    component.adapts(IPersonalSpace)
    interface.implements(IContentWorkspaceFactory)

    name = u'content'
    title = _(u'Your stuff')
    description = u''
    weight = 2
    factory = ContentWorkspace

    def isAvailable(self):
        principal = self.space.principal
        if principal is not None:
            return checkPermissionForPrincipal(
                principal, 'zojax.PersonalContent', self.space)
        else:
            return False

    @property
    def title(self):
        if not self.isInstalled() or self.space.principal.id == getRequest().principal.id:
            return translate(u'Your stuff', 'zojax.personal.content')
        else:
            principal = self.space.principal
            profile = IPersonalProfile(principal)

            return translate("${user_title}'s stuff", 'zojax.personal.content',
                             mapping={'user_title': profile.title})


@component.adapter(IContentWorkspace, IObjectAddedEvent)
def contentWorkspaceAdded(workspace, obevent):
    if 'draft' not in workspace:
        draft = DraftContainer()
        event.notify(ObjectCreatedEvent(draft))
        workspace['draft'] = draft


@component.adapter(IPrincipal)
@interface.implementer(IContentWorkspace)
def getContentWorkspace(principal):
    space = IPersonalSpace(principal, None)
    if space is not None:
        wf = getAdapter(space, IContentWorkspaceFactory, 'content')
        if wf.isAvailable():
            return wf.install()


@component.adapter(IPrincipal, IDraftContentType)
@interface.implementer(IDraftContainer)
def getDraftContainer(principal, dct):
    space = IPersonalSpace(principal, None)
    if space is not None:
        wf = getAdapter(space, IContentWorkspaceFactory, 'content')
        if space.isEnabled(wf):
            ws = wf.install()
            return ws['draft']
