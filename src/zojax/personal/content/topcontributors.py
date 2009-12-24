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
from zope import component
from zojax.ownership.interfaces import IOwnership, IOwnerAware
from zojax.topcontributors.api import contribute
from zojax.content.draft.interfaces import IDraftPublishedEvent


@component.adapter(IOwnerAware, IDraftPublishedEvent)
def draftPublishedHandler(content, event):
    contribute(content, IOwnership(content).ownerId, 5)
