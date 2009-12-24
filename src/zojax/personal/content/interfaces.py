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
""" zojax.workspace.content interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.notifications.interfaces import IContentNotification

_ = MessageFactory('zojax.personal.content')


class IContentWorkspace(IWorkspace):
    """Content workspace."""


class IContentWorkspaceFactory(IWorkspaceFactory):
    """Content workspace factory."""


class IReviewWorkspace(IWorkspace):
    """Workspace for managing submitted content."""


class IReviewWorkspaceFactory(IWorkspaceFactory):
    """Review workspace factory."""


class IDraftNotification(IContentNotification):
    """Draft notifications for managers."""


class IDraftStatusActivityRecord(interface.Interface):
    """ draft status changed """

    status = interface.Attribute('Status')
    comment = interface.Attribute('Comment')


class IDraftPublishedActivityRecord(interface.Interface):
    """ draft published """


class IObjectRetractedActivityRecord(interface.Interface):
    """ object retracted activity record """
