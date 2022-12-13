from __future__ import print_function
from compiler import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    # @addToClass(AST.Node)
    # def printTree(self, indent=0):
    #     raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    # @addToClass(AST.IntNum)
    # def printTree(self, indent=0):
    #     print("|  " * indent, end="")
    #     print(self.value)
    #
    # @addToClass(AST.FloatNum)
    # def printTree(self, indent=0):
    #     print("|  " * indent, end="")
    #     print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print(self.name)

    @addToClass(AST.Value)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print(self.value)

    @addToClass(AST.Operator)
    def printTree(self, indent=0):

        print("|  " * indent, end="")
        print(self.op)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        self.op.printTree(indent)

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnExpr)
    def printTree(self, indent=0):
        # print("|  " * indent, end="")
        self.expr.printTree(indent)
        self.value.printTree(indent + 1)

    @addToClass(AST.CompOp)
    def printTree(self, indent=0):
        self.op.printTree(indent)

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("REF")

        self.name.printTree(indent + 1)
        self.val1.printTree(indent + 1)
        if self.val2 is not None:
            self.val2.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        self.op.printTree(indent)

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("IF")
        self.condition.printTree(indent + 1)

        print("|  " * indent, end="")
        print("THEN")
        self.if_.printTree(indent + 1)

        if self.else_ is not None:
            print("|  " * indent, end="")
            print("ELSE")
            self.else_.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("FOR")

        self.for_expr.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ForExpr)
    def printTree(self, indent=0):
        self.variable.printTree(indent)
        self.range.printTree(indent)

    @addToClass(AST.ForRange)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("RANGE")

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("WHILE")

        self.condition.printTree(indent + 1)
        self.instructions.printTree(indent + 1)

    @addToClass(AST.SysCall)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        # self.name.printTree(indent)
        print(self.name)

        if self.value is not None:
            self.value.printTree(indent)

    @addToClass(AST.PrintInputs)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("PRINT")
        for input in self.inputs:
            input.printTree(indent + 1)

    @addToClass(AST.MatrixFun)
    def printTree(self, indent=0):
        self.name.printTree(indent)
        self.value.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("VECTOR")
        for vector in self.vectors:
            vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("|  " * indent, end="")
        print("VECTOR")
        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        # nie jestem pewna
        exit(0)
