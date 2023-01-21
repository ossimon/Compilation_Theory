import numpy as np

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
    './': operator.truediv
}
comparison_operators = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}
unary_operators = {
    '-': lambda x: -x,
    "'": lambda x: np.transpose(x)
}
matrix_func = {
    'zeros': lambda x: np.zeros(x),
    'ones': lambda x: np.ones(x),
    'eye': lambda x: np.eye(x)
}

# Do zrobienia:
# Variable
# sprawdzić Ref
# Assign
# pętle i if - w nich te zagłębienia
# Calla sprawdzić

class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(AST.Variable)
    def visit(self, node):
        # return memory_stack.get(node.name)
        pass

    @when(AST.Value)
    def visit(self, node):
        return node.value

    @when(AST.Operator)
    def visit(self, node):
        return node.op

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        if r2 == 0 and node.op == '/':
            print('Division by 0 in line', node.lineno)
        return binary_operators[node.op](r1, r2)

    @when(AST.UnExpr)
    def visit(self, node):
        val = node.value.accept(self)
        return unary_operators[node.expr](val)

    @when(AST.Comp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return comparison_operators[node.op](r1, r2)

    @when(AST.Ref)
    def visit(self, node):
        matrix_name = node.name.accept(self)
        index1 = node.val1.accept(self)
        # nie wiem czy mogę wizytować index2 jak jest nonem
        # można to łatwo przeprawić
        index2 = node.val1.accept(self)

        # to by było zbyt piękne gdyby to działało
        if index2 is None:
            return matrix_name[index1]
        return matrix_name[index1, index2]

    @when(AST.Assign)
    def visit(self, node):
        if isinstance(node.left, AST.Variable):
            name = node.left.name

    @when(AST.IfElse)
    def visit(self, node):
        pass

    @when(AST.For)
    def visit(self, node):
        pass

    @when(AST.ForExpr)
    def visit(self, node):
        pass

    @when(AST.ForRange)
    def visit(self, node):
        pass
        if isinstance(node.left, AST.Variable):
            name = node.left.name

    @when(AST.While)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

    @when(AST.Call)
    def visit(self, node):
        # może to rozbić na kilka funkcji?
        if node.name == 'RETURN':
            # nie wiem co zrobić ze zwracaną wartościa
            # i guess kończymy program, printujemy zawarotość
            print(node.value.accept(self))
            # czy nasz return może zwracać kilka rzeczy?
            #chyba nie
            #może można zmargeować z printem xd
            sys.exit()

            # # moja wersja
            # raise ReturnValueException(node.value.accept(self))

        elif node.name == 'PRINT':
            print(*node.value.accept(self))
        elif node.name == 'BREAK':
            raise BreakException
        elif node.name == 'CONTINUE':
            raise ContinueException

    @when(AST.PrintInputs)
    def visit(self, node):
        # nie jestem pewna, bo wywołanie printa jest chybaw callu
        return [imput.accept(self) for imput in node.imputs]

    @when(AST.MatrixFun)
    def visit(self, node):
        val = node.value.accept(self)
        return matrix_func[node.name](val)

    @when(AST.Matrix)
    def visit(self, node):
        return [np.array([vector.accept(self) for vector in node.vectors])]

    @when(AST.Vector)
    def visit(self, node):
        return np.array([value.accept(self) for value in node.values])

