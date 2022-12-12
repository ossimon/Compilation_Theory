
import sys
from compiler.Mparser import *
from compiler.scanner import *

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Lexer()
    lexer.input(text)
    ast = parser.parse(text, lexer=lexer)
    ast.printTree()
