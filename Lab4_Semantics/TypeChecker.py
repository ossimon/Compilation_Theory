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

    def visit_Variable(self, node):
        pass

    def visit_Value(self, node):
        return node.type

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
        self.symbol_table = self.symbol_table.pushScope('FOR')
        instruction = self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()

    def visit_ForExpr(self, node):
        variable = self.visit(node.variable)
        range = self.visit(node.range)

    def visit_ForRange(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

    def visit_While(self, node):
        type1 = self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope('WHILE')
        type2 = self.visit(node.instructions)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Call(self, node):
        if node.name in ['BREAK', 'CONTINUE'] and not self.symbol_table.inLoop():
            print(node.name, 'usage outside of loop in line', node.lineno)
        if node.value is not None:
            value_type = self.visit(node.value)

    def visit_PrintInputs(self, node):
        for inp in node.inputs:
            input_type = self.visit(inp)

    def visit_MatrixFun(self, node):
        fun_name = node.name
        value_type = self.visit(node.value)

    def visit_Matrix(self, node):
        for vector in node.vectors:
            self.visit(vector)

    def visit_Vector(self, node):
        for value in node.values:
            self.visit(value)
