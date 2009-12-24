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
from zojax.content.activity.browser.portletrecord import PortletRecordView

from interfaces import _

messages = {'submitted': _('Draft submitted.'),
            'rejected': _('Draft rejected.'),
            'retracted': _('Draft retracted.')}

messages2 = {'submitted': _('submitted draft'),
             'rejected': _('rejected draft'),
             'retracted': _('retracted draft')}


class DraftStatusRecordView(object):

    def update(self):
        context = self.context

        self.msg = messages.get(context.status, context.status)
        self.comment = context.comment


class DraftPublishedRecordView(object):

    def update(self):
        self.msg = _('Content published.')
        self.comment = self.context.comment


class DraftStatusPortletRecordView(PortletRecordView):

    def update(self):
        super(DraftStatusPortletRecordView, self).update()

        self.verb = messages2.get(self.context.status, self.context.status)
