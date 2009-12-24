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
from zojax.content.actions.interfaces import IAction
from zojax.content.actions.interfaces import IContentAction
from zojax.content.actions.interfaces import IManageContentCategory
from zojax.content.table.interfaces import IContentsTable
from zojax.personal.content.interfaces import _


class ICreateContentAction(IAction):
    """ create content action """


class IRetractContentAction(IContentAction, IManageContentCategory):
    """ retract content """


class IWorkspaceContentType(interface.Interface):
    """Workspace content type."""


class IPersonalContentTable(IContentsTable):
    """ personal content table """


class IPersonalDraftsTable(IContentsTable):
    """ personal drafts table """


class IReviewContentTable(IContentsTable):
    """ review content table """
