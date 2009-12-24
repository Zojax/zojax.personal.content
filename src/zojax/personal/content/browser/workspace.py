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
from zope import interface, component
from zope.component import getMultiAdapter, queryUtility
from zope.publisher.interfaces import NotFound
from zope.contentprovider.interfaces import IContentProvider

from zojax.content.draft.interfaces import IDraftContentType
from zojax.personal.content.interfaces import IContentWorkspace
from zojax.principal.profile.interfaces import IPersonalProfile

from interfaces import _, IWorkspaceContentType, IPersonalContentTable


class WorkspaceView(object):

    principal_title = None

    def label(self):
        if self.principal_title is None:
            return _(u'Your Latest Content')
        else:
            return _("${user_title}'s Latest Content",
                     mapping={'user_title': self.principal_title})

    def description(self):
        if self.principal_title is None:
            return _(u'Below is a list of content items you created.')
        else:
            return _(u'Below is a list of content items ${user_title} created.',
                     mapping={'user_title': self.principal_title})

    def update(self):
        context = self.context
        request = self.request

        principal = context.__parent__.principal

        if principal.id != request.principal.id:
            profile = IPersonalProfile(principal)
            self.principal_title = profile.title

        if principal.id == request.principal.id:
            self.drafts = getMultiAdapter(
                (context, request, self), IContentProvider, 'personal.drafts')
            self.drafts.update()
        else:
            self.drafts = ()


class WorkspacePublisherPlugin(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        ctype = queryUtility(IDraftContentType, name)
        if ctype is not None:
            context = self.context
            ctype = ctype.__bind__(context)
            ctype.__name__ = name
            ctype.__parent__ = context

            interface.directlyProvides(ctype, IWorkspaceContentType)
            return ctype

        if name in self.context:
            return self.context[name]

        raise NotFound(self.context, name, request)
