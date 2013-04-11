# -*- coding: utf-8 -*-
## This file is part of py-import-search.
## Copyright (C) 2013 CERN.
##
## py-import-search is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## py-import-search is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with py-import-search; if not, write to the Free Software Foundation,
## Inc., ## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='py-import-search',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=False,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'py-import-search = pyimportsearch:main',
        ],
    },

    # PyPI metadata
    author="Lars Holm Nielsen",
    author_email="lars.holm.nielsen@cern.ch",
    description=("A small utility for search your source files for specific imports"),
    long_description=read('README.md'),
    license="GPL",
    url="https://github.com/lnielsen-cern/py-import-search",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
