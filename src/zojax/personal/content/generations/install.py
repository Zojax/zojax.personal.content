##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from zope.app.component.interfaces import ISite
from zope.app.zopeappgenerations import getRootFolder
from zope.app.component.site import setSite


def evolve(context):
    root = getRootFolder(context)

    for site in findObjectsMatching(root, ISite.providedBy):
        setSite(site)

        sm = site.getSiteManager()
        cp = sm.get('controlpanel', None)
        if cp is None:
            continue
        data = cp.get('system.activity', None)
        if data is None:
            continue
        catalog = data['catalog']
        keys = []
        for key, val in data.records.items():
            if str(val.__class__) in (
                "<class 'zojax.content.draft.activity.DraftPublishedActivityRecord'>",
                "<class 'zojax.content.draft.activity.DraftStatusActivityRecord'>"):
                keys.append(key)

        for key in keys:
            del data.records[key]

        catalog.clear()
        catalog.updateIndexes()

    setSite(None)


def findObjectsMatching(root, condition):
    if condition(root):
        yield root

    if hasattr(root, 'values') and callable(root.values):
        for subobj in root.values():
            for match in findObjectsMatching(subobj, condition):
                yield match
