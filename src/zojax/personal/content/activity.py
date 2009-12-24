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
from zope.app.intid.interfaces import IIntIds

from zojax.activity.record import ActivityRecord
from zojax.activity.interfaces import IActivity, IActivityAware
from zojax.activity.interfaces import IActivityRecordDescription
from zojax.content.activity.interfaces import IContentActivityRecord

from zojax.content.type.interfaces import IContent
from zojax.content.draft import interfaces

from interfaces import _, \
    IDraftStatusActivityRecord, \
    IDraftPublishedActivityRecord, IObjectRetractedActivityRecord


class DraftStatusActivityRecord(ActivityRecord):
    interface.implements(IDraftStatusActivityRecord)

    type = u'draft-status'


class DraftStatusActivityRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = interfaces._('Draft status')
    description = interfaces._(u'Draft status changed.')


class ObjectRetractedActivityRecord(ActivityRecord):
    interface.implements(IObjectRetractedActivityRecord, IContentActivityRecord)

    verb = _('retracted')
    type = u'draft-object-retracted'


class ObjectRetractedActivityRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = interfaces._('Retracted')
    description = interfaces._(u'Object retracted.')


class DraftPublishedActivityRecord(ActivityRecord):
    interface.implements(IDraftPublishedActivityRecord, IContentActivityRecord)

    type = u'draft-published'
    verb = interfaces._('published')


class DraftPublishedActivityRecordDescription(object):
    interface.implements(IActivityRecordDescription)

    title = interfaces._('Published')
    description = interfaces._('Draft published.')


@component.adapter(IActivityAware, interfaces.IDraftSubmittedEvent)
def draftSubmittedHandler(content, event):
    getUtility(IActivity).add(
        content,
        DraftStatusActivityRecord(
            status = u'submitted', comment = event.comment))


@component.adapter(IActivityAware, interfaces.IDraftRejectedEvent)
def draftRejectedHandler(content, event):
    getUtility(IActivity).add(
        content,
        DraftStatusActivityRecord(
            status = u'rejected', comment = event.comment))


@component.adapter(IActivityAware, interfaces.IDraftRetractedEvent)
def draftRetractedHandler(content, event):
    getUtility(IActivity).add(
        content,
        DraftStatusActivityRecord(
            status = u'retracted', comment = event.comment))


@component.adapter(IActivityAware, interfaces.IDraftPublishedEvent)
def draftPublishedHandler(content, event):
    activity = getUtility(IActivity)
    activity.add(content, DraftPublishedActivityRecord(comment = event.comment))
    activity.updateObjectRecords(content)


@component.adapter(IActivityAware, interfaces.IObjectRetractedEvent)
def objectRetractedHandler(content, event):
    activity = getUtility(IActivity)
    activity.add(content, ObjectRetractedActivityRecord())
    activity.updateObjectRecords(content)
