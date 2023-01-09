#!/usr/bin/python
from collections import defaultdict

#
# class Symbol(object):
#     pass
#
#
# class VariableSymbol(Symbol):
#
#     def __init__(self, name, type):
#         self.name = name
#         self.type = type


class SymbolTable(object):

    def __init__(self, parent=None, name=''): # parent scope and symbol table name
        self.symbols = defaultdict()
        self.parent = parent
        self.name = name

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols.keys():
            return self.symbols[name]

        if self.parent is not None:
            return self.parent.get(name)

        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(parent=self, name=name)

    def popScope(self):
        self.symbols = None
        return self.parent
