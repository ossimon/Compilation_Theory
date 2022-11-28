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

start = 'program'


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : program block
               | block"""


def p_block(p):
    """block : LCURLBRACK block RCURLBRACK
             | LCURLBRACK empty RCURLBRACK
             | block instruction
             | instruction"""


def p_empty(p):
    """empty :"""
    pass


def instruction(p):
    """instruction : assignment SEMICOLON
                   | call SEMICOLON
                   | loop
                   | branch"""

def p_assignment(p):
    """assignment : ID ASSIGN expression
                  | ID ADDASSIGN expression
                  | ID SUBASSIGN expression
                  | ID MULASSIGN expression
                  | ID DIVASSIGN expression"""


def p_call(p):
    """call : sys_call
            | fun_call"""


def p_sys_call(p):
    """sys_call : BREAK
                | CONTINUE
                | RETURN expression"""


def p_fun_call(p):
    """fun_call : fun_name LPARENT expression RPARENT"""


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES
                | PRINT"""


def p_loop(p):
    """loop : for
            | while"""


def p_for(p):
    """for : FOR for_expression block"""


def p_for_expression(p):
    """for_expression : ID ASSIGN term COLON term"""


def p_term(p):
    """term : ID
            | number
            | matrix"""


def p_number(p):
    """number : INT
              | FLOAT"""


def p_matrix(p):
    """matrix : LSQBRACK"""


def p_branch(p):
    """"""

parser = yacc.yacc()
