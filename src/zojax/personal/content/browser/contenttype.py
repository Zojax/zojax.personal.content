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
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.contentprovider.interfaces import IContentProvider

from zojax.batching.batch import Batch
from zojax.content.type.interfaces import IContentType
from zojax.content.draft.browser.adding import AddDraftWizard

from interfaces import ICreateContentAction, IWorkspaceContentType


class ContentTypeView(object):

    def update(self):
        request = self.request
        context = self.context

        principal = context.__parent__.__parent__.principal

        if principal.id == request.principal.id:
            self.drafts = getMultiAdapter(
                (context, request, self), IContentProvider, 'personal.drafts')
            self.drafts.update()
        else:
            self.drafts = ()


class CreateDraft(AddDraftWizard):

    @property
    def title(self):
        return self.ct.title

    def nextURL(self):
        return '%s/'%absoluteURL(self.context, self.request)

    def cancelURL(self):
        return '%s/'%absoluteURL(self.context, self.request)

    def getDraftContainer(self):
        return self.context.__parent__['draft']


class CreateContentAction(object):
    interface.implements(ICreateContentAction)
    component.adapts(IWorkspaceContentType, interface.Interface)

    weight = 100

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.title = u'Create: ' + self.context.title

    def url(self):
        return 'create.html'

    def isAvailable(self):
        return True


@interface.implementer(interface.Interface)
@component.adapter(CreateContentAction, interface.Interface)
def CreateContentActionIcon(action, request):
    return queryMultiAdapter((action.context, request), name='zmi_icon')
