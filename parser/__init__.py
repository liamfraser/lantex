#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CAVEAT UTILITOR
# This file was automatically generated by Grako.
#    https://bitbucket.org/apalala/grako/
# Any changes you make to it will be overwritten the
# next time the file is generated.
#

from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import *  # noqa
from grako.exceptions import *  # noqa
from lantex import types
from copy import deepcopy
import itertools

__version__ = '14.166.15.04.23'


class lantexParser(Parser):
    def __init__(self, whitespace=None, **kwargs):
        super(lantexParser, self).__init__(whitespace=whitespace, **kwargs)

    @rule_def
    def _lower_letter_(self):
        self._pattern(r'[a-z]')

    @rule_def
    def _upper_letter_(self):
        self._pattern(r'[A-Z]')

    @rule_def
    def _letter_(self):
        with self._choice():
            with self._option():
                self._lower_letter_()
            with self._option():
                self._upper_letter_()
            self._error('no available options')

    @rule_def
    def _letters_(self):

        def block0():
            self._letter_()
        self._positive_closure(block0)

    @rule_def
    def _number_(self):
        self._pattern(r'[0-9]')

    @rule_def
    def _numbers_(self):

        def block0():
            self._number_()
        self._positive_closure(block0)

    @rule_def
    def _number_range_(self):
        self._numbers_()
        self._token('-')
        self._numbers_()

    @rule_def
    def _punct_(self):
        self._pattern(r'[!"$%&*+,\-./:;<=>?@ [\\\]^_`|~]')

    @rule_def
    def _text_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._letter_()
                with self._option():
                    self._punct_()
                self._error('no available options')
        self._positive_closure(block0)

    @rule_def
    def _string_(self):
        self._token("'")
        self._text_()
        self._token("'")

    @rule_def
    def _lbrace_(self):
        self._token('{')

    @rule_def
    def _rbrace_(self):
        self._token('}')

    @rule_def
    def _lbrack_(self):
        self._token('(')

    @rule_def
    def _rbrack_(self):
        self._token(')')

    @rule_def
    def _nline_(self):
        self._token('\n')

    @rule_def
    def _primitive_(self):
        self._upper_letter_()
        self._letters_()

    @rule_def
    def _identifier_(self):
        self._letter_()

        def block0():
            with self._choice():
                with self._option():
                    self._letter_()
                with self._option():
                    self._token('_')
                with self._option():
                    self._number_()
                self._error('expecting one of: _')
        self._closure(block0)

    @rule_def
    def _assignment_(self):
        self._token('=')

    @rule_def
    def _space_(self):
        with self._choice():
            with self._option():
                self._token(' ')
            with self._option():
                self._token('\t')
            self._error('expecting one of:   \t')

    @rule_def
    def _spaces_(self):

        def block0():
            self._space_()
        self._closure(block0)

    @rule_def
    def _section_(self):
        self._primitive_()
        self._space_()
        self._identifier_()
        with self._optional():
            self._space_()
        self._lbrace_()
        with self._optional():
            self._nline_()
        self._section_statements_()
        self._rbrace_()

        def block0():
            self._nline_()
        self._positive_closure(block0)

    @rule_def
    def _ip4_(self):
        self._pattern(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

    @rule_def
    def _ip6_(self):
        self._pattern(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

    @rule_def
    def _ipmask_(self):
        self._token('/')
        self._numbers_()

    @rule_def
    def _atype_(self):
        with self._choice():
            with self._option():
                self._identifier_()
            with self._option():
                self._ip4_()
                self._ipmask_()
            with self._option():
                self._ip6_()
                self._ipmask_()
            with self._option():
                self._ip4_()
            with self._option():
                self._ip6_()
            with self._option():
                self._number_range_()
            with self._option():
                self._numbers_()
            with self._option():
                self._string_()
            self._error('no available options')

    @rule_def
    def _notes_(self):
        self._lbrack_()
        self._text_()
        self._rbrack_()

    @rule_def
    def _value_assignment_(self):
        self._identifier_()
        self._spaces_()
        self._assignment_()
        self._spaces_()
        with self._group():
            with self._choice():
                with self._option():
                    self._atype_()
                with self._option():
                    self._map_()
                self._error('no available options')
        with self._optional():
            self._spaces_()
            self._notes_()

    @rule_def
    def _arrow_(self):
        self._token('->')

    @rule_def
    def _access_(self):
        with self._choice():
            with self._option():
                self._identifier_()
                self._arrow_()
                self._access_()
            with self._option():
                self._identifier_()
                self._arrow_()
                self._identifier_()
            self._error('no available options')

    @rule_def
    def _access_assign_(self):
        self._access_()
        self._spaces_()
        self._assignment_()
        self._spaces_()
        self._atype_()
        with self._optional():
            self._spaces_()
            self._notes_()

    @rule_def
    def _connection_(self):
        self._identifier_()
        self._arrow_()
        self._numbers_()

    @rule_def
    def _colon_(self):
        self._token(':')

    @rule_def
    def _next_(self):
        self._token(',')
        with self._optional():
            self._nline_()

    @rule_def
    def _map_entry_(self):
        self._spaces_()
        with self._group():
            with self._choice():
                with self._option():
                    self._numbers_()
                with self._option():
                    self._identifier_()
                self._error('no available options')
        self._spaces_()
        self._colon_()
        self._spaces_()
        with self._group():
            with self._choice():
                with self._option():
                    self._connection_()
                with self._option():
                    self._atype_()
                self._error('no available options')
        self._spaces_()

    @rule_def
    def _map_(self):
        self._lbrace_()

        def block0():
            self._map_entry_()
            self._next_()
        self._closure(block0)
        self._map_entry_()
        self._rbrace_()

    @rule_def
    def _section_statement_(self):
        self._spaces_()
        with self._group():
            with self._choice():
                with self._option():
                    self._value_assignment_()
                with self._option():
                    self._access_assign_()
                with self._option():
                    self._tunnel_route_()
                self._error('no available options')
        self._spaces_()

        def block1():
            with self._choice():
                with self._option():
                    self._nline_()
                with self._option():
                    self._spaces_()
                self._error('no available options')
        self._positive_closure(block1)

    @rule_def
    def _section_statements_(self):

        def block0():
            self._section_statement_()
        self._positive_closure(block0)

    @rule_def
    def _tunnel_route_(self):
        self._token('Tunnel')
        self._space_()
        self._identifier_()
        self._space_()
        self._token('via')
        self._space_()
        self._identifier_()

    @rule_def
    def _start_(self):

        def block0():
            self._section_()
        self._positive_closure(block0)


class lantexSemanticParser(CheckSemanticsMixin, lantexParser):
    pass


class lantexSemantics(object):
    def __init__(self):
        self.entities = []
        self.last_istring = None

    def fail(self, error):
        print(error)
        print(self.last_istring)
        print(self.entities)

    def lower_letter(self, ast):
        return ast

    def upper_letter(self, ast):
        return ast

    def letter(self, ast):
        return ast

    def letters(self, ast):
        return ast

    def number(self, ast):
        return ast

    def numbers(self, ast):
        return ast

    def number_range(self, ast):
        return ast

    def punct(self, ast):
        return ast

    def text(self, ast):
        return ast

    def string(self, ast):
        return ast

    def lbrace(self, ast):
        return ast

    def rbrace(self, ast):
        return ast

    def lbrack(self, ast):
        return ast

    def rbrack(self, ast):
        return ast

    def nline(self, ast):
        return ast

    def primitive(self, ast):
        pstring = "".join(itertools.chain(*ast))

        if pstring in types.primitives:
            new_prim = types.primitives[pstring]()
            self.entities.append(new_prim)
        else:
            self.fail("{0} is not a valid type".format(pstring))

    def identifier(self, ast):
        """
        Identifier matches most text assign types so need to be careful
        """

        old_ast = deepcopy(ast)
        istring = "".join(itertools.chain(*ast))

        # If the latest thing in the entity list is a primitive without an
        # identifier, then set one.
        if self.entities[-1].identifier == None:
            self.entities[-1].identifier = istring
       
        # If it's not an identifier for a new entity, then it might be a property
        # of the entity which will be set once we have the value
        elif self.entities[-1].valid_property(istring) and self.last_istring == None:
            self.last_istring = istring

        # We have found a value that needs to be assigned to something so
        # assign it to the last property if we have one. Otherwise fail.
        elif self.last_istring != None:
            setattr(self.entities[-1], self.last_istring, istring) 
            # Reset last istring
            self.last_istring = None
        
        else:
            self.fail("Unsure what to do with identifier {0}".format(istring))
            return old_ast

    def assignment(self, ast):
        return ast

    def space(self, ast):
        return ast

    def spaces(self, ast):
        return ast

    def section(self, ast):
        return ast

    def ip4(self, ast):
        return ast

    def ip6(self, ast):
        return ast

    def ipmask(self, ast):
        return ast

    def atype(self, ast):
        # We have found a value that needs to be assigned to something so
        # assign it to the last property if we have one. Otherwise fail.

        astring = None

        if self.last_istring != None:
            astring = "".join(itertools.chain(*ast))
            setattr(self.entities[-1], self.last_istring, astring) 
            # Reset last istring
            self.last_istring = None
        
        elif self.last_istring == None:
            # No idea how we get here but we do. We don't have anything to assign
            # an assign type to so do nothing. Seems to be when ast == None
            pass

        else:
            self.fail("Unsure what to do with assign type {0}".format(astring))

    def notes(self, ast):
        return ast

    def value_assignment(self, ast):
        return ast

    def arrow(self, ast):
        return ast

    def access(self, ast):
        return ast

    def access_assign(self, ast):
        return ast

    def connection(self, ast):
        return ast

    def colon(self, ast):
        return ast

    def next(self, ast):
        return ast

    def map_entry(self, ast):
        return ast

    def map(self, ast):
        return ast

    def section_statement(self, ast):
        return ast

    def section_statements(self, ast):
        return ast

    def tunnel_route(self, ast):
        return ast

    def start(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = lantexParser(parseinfo=False)
    semanticsInstance = lantexSemantics()

    ast = parser.parse(
          text,
          startrule,
          filename=filename,
          trace=trace,
          semantics=semanticsInstance,
          whitespace="")
    #print('AST:')
    #print(ast)
    
    return semanticsInstance.entities

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in lantexParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for lantex.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(args.file, args.startrule, trace=args.trace, whitespace=args.whitespace)
