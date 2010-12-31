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
from zojax.content.browser.table import IdColumn
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.content.space.utils import getWorkspace
"""

$Id$
"""
from zope import interface, component
from zope.i18n import translate
from zope.proxy import removeAllProxies
from zope.component import getUtility, getUtilitiesFor

from zojax.table.table import Table
from zojax.table.column import Column
from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IContentType
from zojax.content.draft.interfaces import IDraftContentType, DraftException
from zojax.content.draft.interfaces import ISubmittedDraftContent
from zojax.content.table.location import LocationColumn
from zojax.personal.content.interfaces import IContentWorkspace

from interfaces import _, IWorkspaceContentType, \
    IPersonalContentTable, IPersonalDraftsTable


class PersonalContentTable(Table):
    interface.implements(IPersonalContentTable)
    component.adapts(IContentWorkspace,interface.Interface,interface.Interface)

    name = u'personal.content'
    title = _('Personal content')

    pageSize = 15
    enabledColumns = ('typeicon', 'title', 'location', 'tags', 'modified')

    def initDataset(self):
        context = self.context

        if IWorkspaceContentType.providedBy(context):
            types = (context.__name__,)
            principal = context.__parent__.__parent__.principal
        else:
            principal = context.__parent__.principal
            types = [name for name, ct in getUtilitiesFor(IDraftContentType)]

        self.dataset = getUtility(ICatalog).searchResults(
            sort_on = 'modified', sort_order='reverse',
            owners = {'any_of': (principal.id,),},
            type = {'any_of': types},
            draftContent = {'any_of': (False,)})

    @property
    def msgEmptyTable(self):
        context = self.context
        if IWorkspaceContentType.providedBy(context):
            principal = context.__parent__.__parent__.principal
        else:
            principal = context.__parent__.principal

        if principal.id == self.request.principal.id:
            return _(u'You do not have any content.')
        else:
            return _(u'He/she does not have any content.')


class PersonalDraftsTable(Table):
    interface.implements(IPersonalDraftsTable)
    component.adapts(IContentWorkspace,interface.Interface,interface.Interface)

    title = _('Personal Drafts')
    msgEmptyTable = _(u'You do not have any draft content.')

    pageSize = 0
    enabledColumns = ('id', 'typeicon','title','location','draftstatus','modified')

    updated = False

    def initDataset(self):
        context = self.context

        if IWorkspaceContentType.providedBy(context):
            container = context.__parent__['draft']

            drafts = []
            ctname = context.__name__
            for draft in container.values():
                dct = IContentType(draft, None)
                if dct is None:
                    continue
                if ctname and (dct.name != ctname):
                    continue
                drafts.append(draft)
            self.dataset = drafts
        else:
            container = context['draft']
            self.dataset = list(container.values())
            
    def update(self):
        if self.updated:
            return

        context = getWorkspace(self.context)['draft']
        request = self.request

        if 'form.button.remove' in request:
            ids = request.get('ids')
            if not ids:
                IStatusMessage(request).add(_('Please select draft items.'))
            else:
                for id in ids:
                    if id in context:
                        del context[id]

                IStatusMessage(request).add(
                    _('Selected draft items have been removed.'))

        if 'form.button.publish' in request:
            ids = request.get('ids')
            if not ids:
                IStatusMessage(request).add(_('Please select draft items.'))
            else:
                for id in ids:
                    if id in context:
                        draft = context[id]
                        try:
                            content = draft.publish()
                        except DraftException, err:
                            IStatusMessage(request).add(str(err), 'error')
                            return
                
                        draft = removeAllProxies(draft)
                        del draft.__parent__[draft.__name__]

                IStatusMessage(request).add(
                    _('Selected draft items have been published.'))

        super(PersonalDraftsTable, self).update()

        self.updated = True

             
class DraftIdColumn(IdColumn):

    buttons = True

    def __bind__(self, content, globalenviron, environ):
        return super(IdColumn, self).__bind__(content, globalenviron, environ)


class LocationColumn(LocationColumn):
    component.adapts(interface.Interface, interface.Interface,
                     IPersonalDraftsTable)

    def getLocation(self):
        return self.content.getLocation()


class DraftStatusColumn(Column):
    component.adapts(
        interface.Interface, interface.Interface,
        IPersonalDraftsTable)

    name = 'draftstatus'
    title = _('Status')

    def query(self, default=None):
        status = ISubmittedDraftContent.providedBy(self.content)

        if status:
            return translate(u'Not Yet Approved', 'zojax.personal.content')
        else:
            return translate(u'Draft', 'zojax.personal.content')
