#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Gregorio Robles
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Gregorio Robles <grex@gsyc.urjc.es>
#

import codecs
import os.path
import re
import sys

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_md = os.path.join(here, 'README.md')
version_py = os.path.join(here, 'git2effort', '_version.py')

# Get the package description from the README.md file
with codecs.open(readme_md, encoding='utf-8') as f:
    long_description = f.read()

with codecs.open(version_py, 'r', encoding='utf-8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(name="git2effort",
      description="Calculate development effort from a Git repository",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/gregoriorobles/git2effort",
      version=version,
      author="Gregorio Robles",
      author_email="grex@gsyc.urjc.es",
      license="GPLv3",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Topic :: Software Development',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python :: 3'
      ],
      keywords="effort development repositories analytics git github",
      packages=[
          'git2effort',
      ],
      namespace_packages=[
          'git2effort'
      ],
      setup_requires=[
          'wheel'
      ],
      install_requires=[
          'perceval>=0.12',
          'python-dateutil>=2.6.0',
          'requests>=2.7.0',
          'beautifulsoup4>=4.3.2',
          'feedparser>=5.1.3',
          'dulwich>=0.18.5, <0.19',
          'urllib3>=1.22'
      ],
      scripts=[
          'bin/git2effort'
      ],
      zip_safe=False)
