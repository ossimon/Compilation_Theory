#!/usr/bin/python
from compiler import AST
import SymbolTable


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

    def visit_Program(self, node):
        pass

    def visit_Instructions(self, node):
        pass

    def visit_Varaible(self, node):
        pass

    def visit_Value(self, node):
        pass

    def visit_Operator(self, node):
        pass

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        # ...
        #

    def visit_UnExpr(self, node):
        pass

    def visit_CompOp(self, node):
        pass

    def visit_Ref(self, node):
        pass

    def visit_Assign(self, node):
        pass

    def visit_IfElse(self, node):
        pass

    def visit_For(self, node):
        pass

    def visit_ForExpr(self, node):
        pass

    def visit_ForRange(self, node):
        pass

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
