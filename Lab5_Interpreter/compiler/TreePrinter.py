from __future__ import print_function
from compiler import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def printWIthIndent(value, indent):
    print("|  " * indent, end="")
    print(value)


class TreePrinter:

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        printWIthIndent(self.name, indent)

    @addToClass(AST.Value)
    def printTree(self, indent=0):
        printWIthIndent(self.value, indent)

    @addToClass(AST.Operator)
    def printTree(self, indent=0):
        printWIthIndent(self.op, indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        self.op.printTree(indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnExpr)
    def printTree(self, indent=0):
        self.expr.printTree(indent)
        self.value.printTree(indent + 1)

    @addToClass(AST.Comp)
    def printTree(self, indent=0):
        self.op.printTree(indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        printWIthIndent("REF", indent)

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
        printWIthIndent("IF", indent)
        self.condition.printTree(indent + 1)

        printWIthIndent("THEN", indent)
        self.if_.printTree(indent + 1)

        if self.else_ is not None:
            printWIthIndent("ELSE", indent)
            self.else_.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        printWIthIndent("FOR", indent)

        self.for_expr.printTree(indent + 1)
        self.instruction.printTree(indent + 1)

    @addToClass(AST.ForExpr)
    def printTree(self, indent=0):
        self.variable.printTree(indent)
        self.range.printTree(indent)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        printWIthIndent("RANGE", indent)

        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        printWIthIndent("WHILE", indent)

        self.condition.printTree(indent + 1)
        self.instructions.printTree(indent + 1)

    @addToClass(AST.Call)
    def printTree(self, indent=0):
        printWIthIndent(self.name, indent)

        if self.value is not None:
            self.value.printTree(indent)

    @addToClass(AST.PrintInputs)
    def printTree(self, indent=0):
        printWIthIndent("PRINT", indent)
        for input in self.inputs:
            input.printTree(indent + 1)

    @addToClass(AST.MatrixFun)
    def printTree(self, indent=0):
        self.name.printTree(indent)
        self.value.printTree(indent + 1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        printWIthIndent("VECTOR", indent)
        for vector in self.vectors:
            vector.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        printWIthIndent("VECTOR", indent)
        for value in self.values:
            value.printTree(indent + 1)
