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
from zope import component, interface
from zope.i18n import translate
from zojax.content.browser.breadcrumb import ContentBreadcrumb
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.personal.content.interfaces import IContentWorkspace


class ContentWorkspaceBreadcrumb(ContentBreadcrumb):
    component.adapts(IContentWorkspace, interface.Interface)

    @property
    def name(self):
        principal = self.context.space.principal

        if principal.id == self.request.principal.id:
            return translate(u'Your stuff', 'zojax.personal.content')
        else:
            profile = IPersonalProfile(principal)

            return translate("${user_title}'s stuff", 'zojax.personal.content',
                             mapping={'user_title': profile.title})
