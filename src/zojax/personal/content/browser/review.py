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
from zope import component, interface
from zope.interface import Interface
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL

from zojax.table.table import Table
from zojax.catalog.interfaces import ICatalog
from zojax.catalog.utils import listAllowedRoles
from zojax.content.table import TitleColumn, LocationColumn
from zojax.personal.content.interfaces import IReviewWorkspace

from interfaces import _, IReviewContentTable


class ReviewContentTable(Table):
    interface.implements(IReviewContentTable)
    component.adapts(IReviewWorkspace, Interface, Interface)

    title = _('Review content')

    pageSize = 15
    enabledColumns = ('typeicon', 'title', 'location', 'author', 'modified')

    def update(self):
        super(ReviewContentTable, self).update()

        self.environ['ids'] = getUtility(IIntIds)
        self.environ['url'] = absoluteURL(self.context, self.request)

    def initDataset(self):
        context = self.context
        principal = context.__parent__.principal

        self.dataset = getUtility(ICatalog).searchResults(
            sort_on='modified', sort_order='reverse',
            noPublishing = True, noSecurityChecks=True,
            draftStatus = {'any_of': ('submitted',)},
            draftPublishable = {'any_of': listAllowedRoles(principal, context)})


class TitleColumn(TitleColumn):
    component.adapts(Interface, Interface, IReviewContentTable)

    def contentUrl(self):
        return '%s/%s/'%(self.globalenviron['url'],
                         self.globalenviron['ids'].getId(self.content))


class LocationColumn(LocationColumn):
    component.adapts(Interface, Interface, IReviewContentTable)

    def getLocation(self):
        return self.content.getLocation()
