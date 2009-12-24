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
from zope.location import Location, LocationProxy
from zope.component import getUtility, queryUtility, queryMultiAdapter
from zope.app.intid.interfaces import IIntIds
from zope.traversing.api import getPath
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher

from zojax.cache.tag import SiteTag
from zojax.cache.view import cache
from zojax.cache.keys import Principal

from zojax.catalog.interfaces import ICatalog
from zojax.catalog.utils import listAllowedRoles, getRequest
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.content.draft.interfaces import ISubmittedDraftContent

from interfaces import _, IReviewWorkspace, IReviewWorkspaceFactory


ReviewTag = SiteTag('personal.content.review')

def updateReviewTag(*args):
    ReviewTag.update()

def getReviewKey(instance, object, *args, **kw):
    request = object.request
    principal = object.context.principal

    if request is None or request.principal.id != principal.id:
        return {'principal': 'notself',
                'context': getPath(object.context)}

    else:
        return {'principal': principal.id,
                'context': getPath(object.context)}


class ReviewWorkspace(Location):
    interface.implements(IReviewWorkspace, IBrowserPublisher)

    title = _(u'Review content')

    __name__ = u'review'

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        try:
            draft = getUtility(IIntIds).getObject(int(name))
        except:
            raise NotFound(self, request, name)

        if ISubmittedDraftContent.providedBy(draft) and draft.isPublishable():
            return LocationProxy(draft, self, name)

        raise NotFound(self, request, name)

    def browserDefault(self, request):
        return self, ('index.html',)


class ReviewWorkspaceFactory(object):
    component.adapts(IPersonalSpace)
    interface.implements(IReviewWorkspaceFactory)

    title = _(u'Review content')
    description = u''
    weight = 3
    name='review'

    def __init__(self, context):
        self.context = context
        self.request = getRequest()

    def get(self):
        review = ReviewWorkspace()
        review.__parent__ = self.context

        return review

    install = get

    def uninstall(self):
        pass

    def isInstalled(self):
        return True

    @cache('personal.content.review', ReviewTag, getReviewKey)
    def isAvailable(self):
        principal = self.context.principal

        request = self.request
        if request is None:
            return False

        if request.principal.id != principal.id:
            return False

        catalog = queryUtility(ICatalog)
        if catalog is not None:
            results = catalog.searchResults(
                noPublishing = True, noSecurityChecks=True,
                draftStatus = {'any_of': ('submitted',)},
                draftPublishable = {
                    'any_of': listAllowedRoles(principal, self.context)})
            return bool(results)

        return False
