#!/usr/bin/python
from typing import Tuple
from compiler import AST
from SymbolTable import SymbolTable

t_int = 'INT'
t_float = 'FLOAT'
t_str = "STRING"
t_var = t_str
t_numerical = {t_int, t_float}
t_binary_op_result = {t_int: {t_int: t_int, t_float: t_float}, t_float: {t_int: t_float, t_float: t_float}}

t_matrix_ops = {'.+', '.-', '.*', './'}
t_comparison_ops = {'<', '>', '<=', '>=', '==', '!='}
t_assignment_ops = {'/=', '+=', '-=', '*=', '='}
t_binary_ops = {'+', '-', '*', '/'}
t_unary_ops = {'-', "'"}
t_matrix_function_names = {'zeros', 'ones', 'eye'}

t_matrix = "MATRIX"
t_vector = "VECTOR"

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
        return self.symbol_table.get(node.name)

    def visit_Value(self, node):
        return node.type

    def visit_Operator(self, node):
        return node.op

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)

        if isinstance(type1, Tuple):
            type1, dims1 = type1
        if isinstance(type2, Tuple):
            type2, dims2 = type2

        if op in t_binary_ops:
            if type1 not in t_numerical or type2 not in t_numerical:
                print("Cannot use", op, 'between types', type1, 'and', type2, 'in line', node.lineno)
            elif type1 in t_numerical and type2 in t_numerical:
                return t_binary_op_result[type1][type2]
        elif op in t_matrix_ops:
            if type1 != t_matrix or type2 != t_matrix:
                print("Cannot use", op, 'between types', type1, 'and', type2, 'in line', node.lineno)
            else:
                if dims1 != dims2:
                    print("Cannot use", op, 'between matrixes of size', dims1, 'and', dims2, 'in line', node.lineno)
                else:
                    return t_matrix, dims1
        else:
            print("Something went wrong", node.lineno)

    def visit_UnExpr(self, node):
        type = self.visit(node.value)
        expr = self.visit(node.expr)

    def visit_Comp(self, node):
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
        if type1 is None and op in t_assignment_ops and node.op.op != '=':
            print('Can\'t use', node.op.op, 'operator on an unassigned variable in line', node.lineno)
        self.symbol_table.put(node.left.name, type2)

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
        name = node.name
        value = node.value.value
        value_type = self.visit(node.value)

        if value_type != t_int:
            print("Type", value_type, "cannot be an argument of function", name.op, 'in line', node.lineno)
            return

        return t_matrix, (value, value)

    def visit_Matrix(self, node):
        vector_size = len(node.vectors[0].values)
        for vector in node.vectors:
            vector_type = self.visit(vector)
            if vector_type != t_vector:
                return
            if vector_size != len(vector.values):
                print("Matrix contains vectors of different sizes in line", node.lineno)
                return
        return t_matrix, (len(node.vectors), vector_size)

    def visit_Vector(self, node):
        for value in node.values:
            val_type = self.visit(value)
            if val_type not in t_numerical:
                print("Vector contains nonnumerical value in line", node.lineno)
                return
        return t_vector
