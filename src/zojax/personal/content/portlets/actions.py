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
from zope.security import checkPermission
from zope.component import getAdapters, getMultiAdapter
from zope.traversing.browser import absoluteURL
from zojax.pageelement.interfaces import IPageElement
from zojax.workspace.content.interfaces import _
from zojax.content.ui.actions.interfaces import IContentActions


class ActionsPortlet(object):
    interface.implements(IContentActions)

    def loadElements(self):
        context = self.context
        request = self.request
        view = self.manager.view

        elements = []
        for name, element in getAdapters(
            (context, request, view, self), IPageElement):
            elements.append((element.weight, name, element))

        elements.sort()
        return [(name, element) for o, name, element in elements]

    def update(self):
        # get main context
        layout = getattr(self.manager, 'view', None)
        if layout is not None:
            self.context = layout.maincontext

        self.elements = [element for name, element in self.loadElements()]

        super(ActionsPortlet, self).update()

    def isAvailable(self):
        return bool(self.elements)
