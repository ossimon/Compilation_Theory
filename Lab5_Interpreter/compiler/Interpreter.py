
from compiler import AST
from compiler import SymbolTable
from compiler.Memory import *
from compiler.Exceptions import  *
from compiler.visit import *
import operator
import sys

sys.setrecursionlimit(10000)

binary_operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '.+': operator.add,
    '.-': operator.sub,
    '.*': operator.mul,
    './': operator.truediv,
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
}

class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if r2 == 0 and node.op == '/':
            print('Division by 0 in line', node.lineno)
        return binary_operators[node.op](r1, r2)

    @when(AST.Assign)
    def visit(self, node):
        if isinstance(node.left, AST.Variable):
            name = node.left.name


    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

