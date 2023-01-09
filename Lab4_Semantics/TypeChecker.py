#!/usr/bin/python
from compiler import AST
from SymbolTable import SymbolTable


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(name='global')

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Varaible(self, node):
        pass

    def visit_Value(self, node):
        pass

    def visit_Operator(self, node):
        pass

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)
        # ...
        #

    def visit_UnExpr(self, node):
        type = self.visit(node.value)
        expr = self.visit(node.expr)

    def visit_CompOp(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)

    def visit_Ref(self, node):
        name = self.visit(node.name)
        val1 = self.visit(node.val1)
        val2 = self.visit(node.val2)

    def visit_Assign(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)

    def visit_IfElse(self, node):
        condition = self.visit(node.condition)


    def visit_For(self, node):
        for_expr = self.visit(node.for_expr)
        instruction = self.visit(node.instruction)

    def visit_ForExpr(self, node):
        variable = self.visit(node.variable)
        range = self.visit(node.range)

    def visit_ForRange(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

    def visit_While(self, node):
        pass

    def visit_Call(self, node):
        pass

    def visit_PrintInputs(self, node):
        pass

    def visit_MatrixFun(self, node):
        pass

    def visit_Matrix(self, node):
        pass

    def visit_Vector(self, node):
        pass
