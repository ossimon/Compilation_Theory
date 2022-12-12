
class Node(object):
    pass
    # count = 0

    # def __init__(self, children=None):
    #     # self.ID = str(Node.count)
    #     # Node.count += 1
    #
    #     if children is None:
    #         self.children = []
    #
    #     elif hasattr(children, '__len__ '):
    #         self.children = children
    #     else:
    #         self.children = [children]


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, instructions):
        if hasattr(instructions, '__len__'):
            self.instructions = instructions
        else:
            self.instructions = [instructions]


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):

    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right


class UnExpr(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class CompOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Ref(Node):
    def __init__(self, name, val1, val2=None):
        self.name = name
        self.val1 = val1
        self.val2 = val2


class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class IfElse(Node):
    def __init__(self, condition, if_, else_):
        self.condition = condition
        self.if_ = if_
        self.else_ = else_


class For(Node):
    def __init__(self, variable, left_range, right_range, instructions):
        self.variable = variable
        self.left_range = left_range
        self.right_range = right_range
        self.instructions = instructions


class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions


class SysCall(Node):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value # optional, only for 'return value;'


class Print(Node):
    def __init__(self, value):
        self.value = value


class Matrix(Node):
    def __init__(self, values):
        self.values = values


class Error(Node):
    def __init__(self):
        pass
