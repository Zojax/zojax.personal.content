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
from zope import interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zojax.content.actions.contentactions import ContentAction
from zojax.content.draft.interfaces import \
    IContentType, IDraftContentType, IDraftedContentType
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, IRetractContentAction


class RetractContentAction(ContentAction):
    interface.implements(IRetractContentAction)

    weight = 100
    action = 'retract.html'
    actionTitle = _('Retract')

    def isAvailable(self):
        if not IDraftedContentType.providedBy(self.contenttype):
            return False

        dct = getUtility(IDraftContentType, self.contenttype.name)

        return dct.__bind__(self.context).isRetractable()


class RetractContent(object):

    def update(self):
        context = self.context
        request = self.request

        ct = IContentType(context)

        if IDraftedContentType.providedBy(ct):
            dct = getUtility(IDraftContentType, ct.name).__bind__(context)

            if dct.isRetractable():
                if 'form.retract.content' in request:
                    content = dct.retract()
                    self.redirect('%s/'%absoluteURL(content, request))
                    IStatusMessage(
                        request).add(_('Content has been retracted.'))

                elif 'form.retract.cancel' in request:
                    self.redirect('./')

                return

        IStatusMessage(request).add(_('Content cannot be retracted.'))
        self.redirect('../')
