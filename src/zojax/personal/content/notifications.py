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
from zope.component import getUtility
from zope.app.component.interfaces import ISite
from zojax.catalog.interfaces import ICatalog
from zojax.catalog.utils import getRequest, listAllowedRoles
from zojax.subscription.interfaces import ISubscriptionDescription
from zojax.content.draft.interfaces import IDraftStatusEvent
from zojax.content.draft.interfaces import IDraftSubmittedEvent
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification

from interfaces import _, IDraftNotification


@component.adapter(ISite)
@interface.implementer(IDraftNotification)
def getDraftNotification(context):
    request = getRequest()
    if request is not None:
        principal = request.principal
        results = getUtility(ICatalog).searchResults(
            noPublishing = True, noSecurityChecks=True,
            draftPublishTo = {'any_of': listAllowedRoles(principal, context)})

        if bool(results):
            return DraftNotification(context)


class DraftNotification(Notification):
    component.adapts(ISite)
    interface.implementsOnly(IDraftNotification)

    type = u'draft'
    title = _(u'Draft')
    description = _(u'Draft events notifications.')


class DraftNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    title = _(u'Forum')
    description = _(u'Forum discussions.')


@component.adapter(interface.Interface, IDraftSubmittedEvent)
def draftStatusChanged(object, ev):
    sendNotification('draft', object, ev)
