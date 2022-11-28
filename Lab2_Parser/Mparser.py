#!/usr/bin/python

import scanner
import ply.yacc as yacc
import numpy as np

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


def p_instruction(p):
    """instruction : assignment SEMICOLON
                   | call SEMICOLON
                   | loop
                   | branch"""


# instrukcję przypisania, w tym różne operatory przypisania
def p_assignment(p):
    """assignment : ID assignment_operator expression"""


def p_assignment_operator(p):
    """assignment_operator : ASSIGN
                           | ADDASIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""

    p[0] = p[1]


def p_call(p):
    """call : sys_call
            | fun_call"""


# instrukcje break, continue oraz return
def p_sys_call(p):
    """sys_call : BREAK
                | CONTINUE
                | RETURN expression"""


def p_fun_call(p):
    """fun_call : fun_name LPARENT expression RPARENT"""


# macierzowe funkcje specjalne, instrukcję print
def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES
                | PRINT"""


# pętle: while and for
def p_loop(p):
    """loop : for
            | while"""


def p_for(p):
    """for : FOR for_expression block"""


def p_for_expression(p):
    """for_expression : ID ASSIGN term COLON term"""


def p_while(p):
    """while : WHILE LPARENT comparison RPARENT block"""


# instrukcję warunkową if-else
def p_branch(p):
    """branch : IF LPARENT comparison RPARENT block %prec IF
              | IF LPARENT comparison RPARENT block ELSE block"""


def p_term(p):
    """term : ID
            | number
            | matrix"""


def p_number(p):
    """number : INT
              | FLOAT"""


# inicjalizację macierzy konkretnymi wartościami
def p_matrix(p):
    """matrix : LSQBRACK matrix_contents RSQBRACK"""


def p_matrix_contents(p):
    """matrix_contents : matrix_contents COMMA matrix_content
                       | matrix_content"""


def p_matrix_content(p):
    """matrix_content : matrix
                      | term
                      | empty"""


def p_expression_term(p):
    """expression : term"""


# wyrażenia binarne, w tym operacje macierzowe 'element po elemencie'
def p_expresson_binary(p):
    """expression : expression binary_operator expression"""


def p_expression_binary(p):
    """expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '.+':
        p[0] = p[1] + p[3]
    elif p[2] == '.-':
        p[0] = p[1] - p[3]
    elif p[2] == '.*':
        p[0] = p[1] * p[3]
    elif p[2] == './':
        p[0] = p[1] / p[3]


def p_binary_operator(p):
    """binary_operator : ADD
                       | SUB
                       | MUL
                       | DIV
                       | DOTADD
                       | DOTSUB
                       | DOTMUL
                       | DOTDIV"""

    p[0] = p[1]


# wyrażenia relacyjne
def p_comparison(p):
    """comparison : expression comparison_operator expression"""

    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]


def p_comparison_operator(p):
    """comparison_operator : SMALLER
                          | LARGER
                          | SMALLEREQ
                          | LARGEREQ
                          | NOTEQ
                          | EQ"""

    p[0] = p[1]


# negację unarną
def p_expression_negation(p):
    """expression : SUB expression %prec UMINUS"""
    p[0] = -p[2]


# transpozycję macierzy
def p_expression_transpose(p):
    """expression : expression TRANSPOSE"""
    p[0] = np.transpose(p[1])


parser = yacc.yacc()
