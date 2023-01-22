#!/usr/bin/python
from typing import Tuple
from compiler import AST
from compiler.SymbolTable import SymbolTable

t_int = 'INT'
t_float = 'FLOAT'
t_str = "STRING"
t_bool = "BOOL"
t_var = t_str
t_numerical = {t_int, t_float}
t_binary_op_result = {t_int: {t_int: t_int, t_float: t_float},
                      t_float: {t_int: t_float, t_float: t_float}}

t_int_vector = "VECTOR"
t_float_vector = "VECTOR"
t_vector = {t_int_vector, t_float_vector}

t_int_matrix = "MATRIX"
t_float_matrix = "MATRIX"
t_matrix = {t_int_matrix, t_float_matrix}
t_binary_op_matrix_result = {t_int_matrix: {t_int_matrix: t_int_matrix, t_float_matrix: t_float_matrix},
                             t_float_matrix: {t_int_matrix: t_float_matrix, t_float_matrix: t_float_matrix}}

t_matrix_ops = {'.+', '.-', '.*', './'}
t_comparison_ops = {'<', '>', '<=', '>=', '==', '!='}
t_assignment_ops = {'/=', '+=', '-=', '*=', '='}
t_binary_ops = {'+', '-', '*', '/'}
t_unary_ops = {'-'}
t_unary_matrix_ops = {'-', "'"}
t_matrix_function_names = {'zeros', 'ones', 'eye'}

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
                if op == "*":
                    if t_str in [type1, type2] and t_int in [type1, type2]:
                        return t_str
                print("Cannot use", op, 'between types', type1, 'and', type2, 'in line', node.lineno)
            else:
                return t_binary_op_result[type1][type2]
        elif op in t_matrix_ops:
            if type1 not in t_matrix or type2 not in t_matrix:
                print("Cannot use", op, 'between types', type1, 'and', type2, 'in line', node.lineno)
            else:
                if dims1 != dims2:
                    print("Cannot use", op, 'between matrixes of size', dims1, 'and', dims2, 'in line', node.lineno)
                else:
                    return t_binary_op_matrix_result[type1][type2], dims1
        elif op in t_comparison_ops:
            if type1 not in t_numerical or type2 not in t_numerical:
                print("Cannot use", op, 'between types', type1, 'and', type2, 'in line', node.lineno)
            else:
                return t_bool
        else:
            print("Something went wrong", node.lineno)

    def visit_UnExpr(self, node):
        type = self.visit(node.value)
        expr = self.visit(node.expr)

        if isinstance(type, Tuple):
            type, dims = type

        if expr in t_unary_ops:
            if type in t_numerical:
                return type
        if expr in t_unary_matrix_ops:
            if type in t_matrix:
                return type, dims
        print("Cannot use", expr, 'on object of type', type, 'in line', node.lineno)

    def visit_Comp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        self.visit(node.op)

    def visit_Ref(self, node):
        matrix_type = self.visit(node.name)
        index1_type = self.visit(node.val1)
        if node.val2 is None:
            index2_type = t_int
        else:
            index2_type = self.visit(node.val2)

        if not isinstance(matrix_type, Tuple):
            print(matrix_type, ' object is not subscriptable in line', node.lineno)
            return

        matrix_type, matrix_dims = matrix_type

        if index1_type != t_int:
            print((matrix_type, matrix_dims), 'indices must be integers, not ', index1_type, 'in line', node.lineno)
            return
        if index2_type != t_int:
            print((matrix_type, matrix_dims), 'indices must be integers, not ', index2_type, 'in line', node.lineno)
            return

        if isinstance(node.val1, AST.Value):
            val1 = node.val1.value
        else:
            # macierz inicjalizowana zmiennymi
            return t_float
        # val2 = node.val2
        if isinstance(node.val2, AST.Value):
            val2 = node.val2.value
        elif node.val2 is None:
            return t_float
        else:
            # macierz inicjalizowana zmiennymi
            return t_float


        if matrix_dims[0] == 1:
            if node.val2 is not None:
                # odwolywanie sie do 2 wymiaru macierzy 1 wymiarowej
                print((matrix_type, matrix_dims), 'index out of range in line', node.lineno)
            elif val1 >= matrix_dims[0]:
                print((matrix_type, matrix_dims), 'index out of range in line', node.lineno)

        elif val1 >= matrix_dims[0] or val2 >= matrix_dims[1]:
            print((matrix_type, matrix_dims), 'index out of range in line', node.lineno)

        if matrix_type == t_float_matrix:
            return t_float
        return t_int

    def visit_Assign(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = self.visit(node.op)
        if type1 is None and op in t_assignment_ops and node.op.op != '=':
            print('Can\'t use', node.op.op, 'operator on an unassigned variable in line', node.lineno)
        self.symbol_table.put(node.left.name, type2)

    def visit_IfElse(self, node):
        self.visit(node.condition)


    def visit_For(self, node):
        self.visit(node.for_expr)
        self.symbol_table = self.symbol_table.pushScope('FOR')
        self.visit(node.for_expr)
        self.visit(node.instruction)
        self.symbol_table = self.symbol_table.popScope()

    def visit_ForExpr(self, node):
        self.visit(node.variable)
        self.visit(node.range)
        self.symbol_table.put(node.variable.name, t_int)

    def visit_Range(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_While(self, node):
        self.symbol_table = self.symbol_table.pushScope('WHILE')
        self.visit(node.instructions)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Call(self, node):
        if node.name in ['BREAK', 'CONTINUE'] and not self.symbol_table.inLoop():
            print(node.name, 'usage outside of loop in line', node.lineno)
        if node.value is not None:
            self.visit(node.value)

    def visit_PrintInputs(self, node):
        for inp in node.inputs:
            self.visit(inp)

    def visit_MatrixFun(self, node):
        name = node.name
        value = node.value.value
        value_type = self.visit(node.value)

        if value_type != t_int:
            print("Type", value_type, "cannot be an argument of function", name.op, 'in line', node.lineno)
            return

        return t_int_matrix, (value, value)

    def visit_Matrix(self, node):
        float_matrix = False
        vector_size = len(node.vectors[0].values)
        for vector in node.vectors:
            vector_type = self.visit(vector)
            if vector_type not in t_vector:
                return
            if vector_type == t_float_vector:
                float_matrix = True
            if vector_size != len(vector.values):
                print("Matrix contains vectors of different sizes in line", node.lineno)
                return
        if float_matrix:
            return t_float_matrix, (len(node.vectors), vector_size)
        return t_int_matrix, (len(node.vectors), vector_size)

    def visit_Vector(self, node):
        float_vector = False
        for value in node.values:
            val_type = self.visit(value)
            if val_type not in t_numerical:
                print("Vector contains nonnumerical value in line", node.lineno)
                return
            if val_type == t_float:
                float_vector = True

        if float_vector:
            return t_float_vector
        return t_int_vector
