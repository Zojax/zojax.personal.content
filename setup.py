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
""" Setup for zojax.personal.content package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='0'


setup(name = 'zojax.personal.content',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Personal content workspace",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax', 'zojax.personal'],
      install_requires = ['setuptools',
                          'zojax.cache',
                          'zojax.content.type',
                          'zojax.content.draft',
                          'zojax.content.forms',
                          'zojax.content.tagging',
                          'zojax.content.permissions',
                          'zojax.content.activity',
                          'zojax.content.actions',
                          'zojax.content.table',
                          'zojax.content.notifications',
                          'zojax.personal.space',
                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.statusmessage',
                          'zojax.security',
                          ],
      extras_require = dict(test=['zojax.personal.space [test]',
                                  'zojax.personal.profile',
                                  'zojax.autoinclude',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
