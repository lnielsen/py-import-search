py-import-search
================

Utility to search Python source files for imports matching given patterns.

Installation
------------

```
pip install py-import-search
```

Usage
-----

```
usage: py-import-search [-h] [-p --pattern PATTERN] [-d --dir DIR]
                        [-r --recursive] [-e --exclude-module MODULE]

Search Python source files for imports

optional arguments:
  -h, --help            show this help message and exit
  -p --pattern PATTERN  pattern for matching imports (multiple allowed).
  -d --dir DIR          path of directory containing Python source files.
  -r --recursive        read all source files under each directory,
                        recursively.
  -e --exclude-module MODULE
                        exclude module (multiple allowed).
```

Examples
--------
Print all imports for source files in a directory:
```
$ py-import-search -d .
.../src/py-import-search/setup.py: from setuptools import find_packages
.../src/py-import-search/setup.py: from setuptools import setup
.../src/py-import-search/setup.py: import os
```

Print all imports for source files in a directory all subdirectories:
```
$ py-import-search -d . -r
.../src/py-import-search/setup.py: from setuptools import find_packages
.../src/py-import-search/setup.py: from setuptools import setup
.../src/py-import-search/setup.py: import os
.../src/py-import-search/src/pyimportsearch/__init__.py: import argparse
.../src/py-import-search/src/pyimportsearch/__init__.py: import ast
.../src/py-import-search/src/pyimportsearch/__init__.py: import os
.../src/py-import-search/src/pyimportsearch/__init__.py: import re
```

Print imports matching 'setup':
```
$ py-import-search -d . -p setup
.../src/py-import-search/setup.py: from setuptools import find_packages
.../src/py-import-search/setup.py: from setuptools import setup
```

Print imports matching 'setup$':
```
$ py-import-search -d . -p 'setup$'
.../src/py-import-search/setup.py: from setuptools import setup
```

Print imports matching 'setup$':
```
$ py-import-search -d . -p 'setup$'
.../src/py-import-search/setup.py: from setuptools import setup
```

Print all imports for source files in a directory excluding os module:
```
$ py-import-search -d . -e os
.../src/py-import-search/setup.py: from setuptools import find_packages
.../src/py-import-search/setup.py: from setuptools import setup
```
