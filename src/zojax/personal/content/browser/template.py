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
import time
from email.Utils import formataddr

from zope import component
from zope.component import getUtility, getMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.catalog.utils import getRequest
from zojax.ownership.interfaces import IOwnership
from zojax.mailtemplate.interfaces import IMailTemplate
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.content.draft.interfaces import \
    IDraftRejectedEvent, IDraftPublishedEvent


class NotificationMail(object):

    space = u''

    def update(self):
        super(NotificationMail, self).update()

        content = self.context
        event = self.contexts[0]
        request = self.request

        self.url = '%s/'%absoluteURL(content, request)

        principal = IOwnership(content).owner

        profile = IPersonalProfile(principal)
        if profile.email:
            author = profile.title
            self.author = author
            self.addHeader(u'From', formataddr((author, profile.email),))
            self.addHeader(u'To', formataddr((self.author, profile.email),))
        else:
            self.author = principal.title or principal.id

        self.site = getSite()

        if profile.space is not None:
            self.space = u'%s/'%absoluteURL(profile.space, request)

        cId = getUtility(IIntIds).getId(content)

        self.messageId = u'<%s.%s@zojax.net>'%(cId, time.time())

    @property
    def subject(self):
        return u'New content has been submitted: %s'%self.context.title


class StatusNotificationMail(object):

    def update(self):
        super(StatusNotificationMail, self).update()

        event = self.context
        request = self.request

        draft = event.draft
        self.draft = event.draft

        self.url = '%s/'%absoluteURL(draft, request)

        principal = IOwnership(draft).owner

        profile = IPersonalProfile(principal)
        if profile.email:
            author = profile.title
            self.author = author
            self.addHeader(u'To', formataddr((self.author, profile.email),))
        else:
            self.author = principal.title or principal.id

        cId = getUtility(IIntIds).getId(draft)

        self.site = getSite()
        self.messageId = u'<%s.%s@zojax.net>'%(cId, time.time())
        self.title = draft.content.title
        self.comment = event.comment


class RejectedNotificationMail(StatusNotificationMail):

    @property
    def subject(self):
        return u'Your content has been rejected: %s'%self.title


@component.adapter(IDraftRejectedEvent)
def draftRejectedHandler(event):
    draft = event.draft

    profile = IPersonalProfile(IOwnership(draft).owner, None)
    if profile and profile.email:
        template = getMultiAdapter((event, getRequest()), IMailTemplate)
        template.send((profile.email,))


class PublishedNotificationMail(StatusNotificationMail):

    def update(self):
        super(PublishedNotificationMail, self).update()

        self.url = '%s/'%absoluteURL(self.context.object, self.request)

    @property
    def subject(self):
        return u'Your content has been published: %s'%self.title


@component.adapter(IDraftPublishedEvent)
def draftPublishedHandler(event):
    draft = event.draft

    ownership = IOwnership(draft, None)
    if ownership is None:
        return

    profile = IPersonalProfile(ownership.owner, None)
    if profile and profile.email:
        request = getRequest()
        if request.principal.id != owner.id:
            template = getMultiAdapter((event, request), IMailTemplate)
            template.send((profile.email,))
