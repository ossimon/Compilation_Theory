
class Node(object):
    def __init__(self, children=None):
        self.lineno = -1
        if children is None:
            self.children = []
        elif hasattr(children, '__len__'):
            self.children = children
        else:
            self.children = [children]


class Program(Node):
    def __init__(self, instructions):
        super().__init__()
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instructions):
        super().__init__()
        if hasattr(instructions, '__len__'):
            self.instructions = instructions
        else:
            self.instructions = [instructions]


class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name


class Value(Node):
    def __init__(self, type, value):
        super().__init__()
        self.type = type
        self.value = value


class Operator(Node):
    def __init__(self, op):
        super().__init__()
        self.op = op


class BinExpr(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right


class UnExpr(Node):
    def __init__(self, value, expr):
        super().__init__()
        self.value = value
        self.expr = expr


class Comp(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right


class Ref(Node):
    def __init__(self, name, val1, val2=None):
        super().__init__()
        self.name = name
        self.val1 = val1
        self.val2 = val2


class Assign(Node):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right


class IfElse(Node):
    def __init__(self, condition, if_, else_=None):
        super().__init__()
        self.condition = condition
        self.if_ = if_
        self.else_ = else_


class For(Node):
    def __init__(self, for_expr, instruction):
        super().__init__()
        self.for_expr = for_expr
        self.instruction = instruction


class ForExpr(Node):
    def __init__(self, variable, for_range):
        super().__init__()
        self.variable = variable
        self.range = for_range


class ForRange(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right


class While(Node):
    def __init__(self, condition, instructions):
        super().__init__()
        self.condition = condition
        self.instructions = instructions


class Call(Node):
    def __init__(self, name, value=None):
        super().__init__()
        self.name = name
        self.value = value


class PrintInputs(Node):
    def __init__(self, inputs):
        super().__init__()
        if hasattr(inputs, '__len__'):
            self.inputs = inputs
        else:
            self.inputs = [inputs]


class MatrixFun(Node):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value


class Matrix(Node):
    def __init__(self, vectors):
        super().__init__()
        if hasattr(vectors, '__len__'):
            self.vectors = vectors
        else:
            self.vectors = [vectors]


class Vector(Node):
    def __init__(self, values):
        super().__init__()
        if hasattr(values, '__len__'):
            self.values = values
        else:
            self.values = [values]
