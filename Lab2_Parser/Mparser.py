#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IF'),
    ('nonassoc', 'SMALLER', 'LARGER', 'SMALLEREQ', 'LARGEREQ', 'NOTEQ', 'EQ', 'ELSE'),
    ('nonassoc', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'), # inni tego nie maja, usunac i w tescie zrobic a = b = c
    # inicjalizacja macierzy konkretnymi wartosciami, tak jak wyzej?
    ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
    ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
    ('left', 'UMINUS'),
    ('right', 'TRANSPOSE') # ????
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


# to finish the grammar
# ....


parser = yacc.yacc()
