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

"""
Utility to search Python source files for imports matching given patterns.
"""

import os
import ast
import argparse
import re


class ImportSearchVisitor(ast.NodeVisitor):
    """
    Visitor that will do a pre-order traversal of the abstract syntax tree,
    detecting any import statements in the source code.
    """
    def __init__(self, patterns):
        self.found = []
        self.found_set = {}
        self.patterns = patterns

    def add_found(self, s):
        self.found.append(s)
        if s in self.found_set:
            self.found_set[s] += 1
        else:
            self.found_set[s] = 1

    def match_module(self, module_str):
        ms = module_str.split(".")
        if not self.patterns:
            return True
        for p in self.patterns:
            for m in ms:
                if p.match(m):
                    return True

    def match(self, from_str, import_strs):
        from_matched = False
        if from_str and self.match_module(from_str):
            from_matched = True

        for alias in import_strs:
            if from_matched:
                self.add_found('from %s import %s' % (from_str, alias.name))
            else:
                if self.match_module(alias.name):
                    if from_str:
                        self.add_found('from %s import %s' % (from_str,
                                                              alias.name))
                    else:
                        self.add_found('import %s' % alias.name)

    def visit_ImportFrom(self, stmt):
        self.match(stmt.module, stmt.names)
        super(ImportSearchVisitor, self).generic_visit(stmt)

    def visit_Import(self, stmt):
        self.match(None, stmt.names)
        super(ImportSearchVisitor, self).generic_visit(stmt)


def search_dir(path, patterns, recursive=False):
    """
    Search imports matching one or more patterns
    in all Python source files.
    """

    files = os.listdir(path)
    subfolders = []

    for f in files:
        filepath = os.path.join(path, f)
        # Collect subfolders if we search recursively
        if recursive and os.path.isdir(filepath):
            subfolders.append(filepath)
            continue

        # Detect and analyze python source files
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == ".py":
            visitor = ImportSearchVisitor(patterns)
            try:
                # Parse source file and search AST with visitor
                visitor.visit(ast.parse(open(filepath).read()))
                visitor.found.sort()
                for importstr in visitor.found:
                    print "%s: %s" % (filepath, importstr)
            except SyntaxError:
                print "ERROR: %s: Syntax Error"

    # Recursively search subfolders (paths only get added, if recursive==True)
    for s in subfolders:
        search_dir(s, patterns, recursive=recursive)


def main():
    """
    Search Python source files for imports
    """
    parser = argparse.ArgumentParser(
        description='Search imports in Python source files'
    )
    parser.add_argument(
        '-p --pattern', metavar='PATTERN', dest='patterns', type=str,
        action='append', help='pattern for matching imports (multiple allowed)'
    )
    parser.add_argument(
        '-d --dir', metavar='DIR', dest='dir', type=str,
        help='path of directory containing Python source files'
    )
    parser.add_argument(
        '-r --recursive', dest='recursive', action='store_true',
        help=' read all source files under each directory, recursively.'
    )

    # Parse arguments
    args = parser.parse_args()
    if not args.dir:
        args.dir = os.getcwd()

    args.dir = os.path.expanduser(args.dir)
    args.dir = os.path.expandvars(args.dir)
    args.dir = os.path.abspath(args.dir)

    if not os.path.exists(args.dir):
        print "ERROR: %s does not exists." % args.dir
        print parser.print_help()
        return 1

    def _re_compile(p):
        try:
            return re.compile(p)
        except Exception:
            raise Exception("Invalid pattern %s" % p)

    if not args.patterns:
        args.patterns = []
    try:
        args.patterns = map(lambda p: re.compile(p), args.patterns)
    except Exception, e:
        print "ERROR: %s" % e.args[0]
        print parser.print_help()
        return 2

    search_dir(args.dir, args.patterns, recursive=args.recursive)


if __name__ == "__main__":
    main()
