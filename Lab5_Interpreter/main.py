

import sys
from compiler.Mparser import *
from compiler.scanner import *
from compiler.TypeChecker import TypeChecker
from compiler.Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/for_example.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Lexer()
    lexer.input(text)
    ast = parser.parse(text, lexer=lexer)
    if ast is not None:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)

        interpreter = Interpreter()
        interpreter.visit(ast)
