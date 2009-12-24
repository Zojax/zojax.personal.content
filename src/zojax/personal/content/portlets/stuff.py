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
from zope.component import getUtility, queryMultiAdapter, getUtilitiesFor
from zope.security import checkPermission
from zope.app.component.hooks import getSite
from zope.traversing.browser import absoluteURL
from zojax.catalog.interfaces import ICatalog
from zojax.catalog.utils import listAllowedRoles
from zojax.content.draft.interfaces import IDraftContentType
from zojax.personal.content.interfaces import IContentWorkspace
from zojax.personal.content.browser.contenttype import CreateDraft


class YourStuffPortlet(object):
    """ VERY IMPORTANT! We need caching for this view """

    view = None

    def isAvailable(self):
        if self.container is None:
            return False
        return self.container.__parent__.principal.id == \
            self.request.principal.id \
            and (not isinstance(getattr(self.view, 'wizard', None), CreateDraft))

    def update(self):
        request = self.request
        container = self.__parent__

        while not IContentWorkspace.providedBy(container):
            container = getattr(container, '__parent__', None)
            if container is None:
                break

        self.container = container
        self.url = absoluteURL(container, request)

        # search draft content type
        layout = getattr(self.manager, 'view', None)
        if layout is not None:
            context = layout.maincontext
            self.view = layout.mainview

            while not IDraftContentType.providedBy(context):
                context = getattr(context, '__parent__', None)
                if context is None:
                    break

            if context is not None:
                self.context = context

        super(YourStuffPortlet, self).update()

    def addingInfo(self):
        request = self.request
        url = self.url

        if IDraftContentType.providedBy(self.context):
            curname = self.context.__name__
        else:
            curname = u''

        ctool = getUtility(ICatalog)
        allowed = listAllowedRoles(self.request.principal, getSite())

        result = []
        for name, ptype in getUtilitiesFor(IDraftContentType):
            permissions = []
            for id in allowed:
                permissions.append((ptype.publish, id))
                permissions.append((ptype.submit, id))

            results = ctool.searchResults(
                noPublishing = True, noSecurityChecks = True,
                draftSubmitTo={'any_of': permissions})

            if not results:
                continue

            action = '%s/%s/'%(url, ptype.name)

            result.append(
                {'id': ptype.name,
                 'title': ptype.title,
                 'description': ptype.description,
                 'action': action,
                 'icon': queryMultiAdapter(
                        (ptype.contenttype, request), name='zmi_icon'),
                 'selected': ptype.name == curname})

        result.sort(lambda a, b: cmp(a['title'], b['title']))
        return result
