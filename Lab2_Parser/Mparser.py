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
                           | ADDASSIGN
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
    """fun_call : matrix_fun
                | print"""


def p_matrix_fun(p):
    """matrix_fun : fun_name LPARENT number_expression RPARENT"""


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES"""


def p_print(p):
    """print : PRINT LPARENT string_expression RPARENT"""


# pętle: while and for
def p_loop(p):
    """loop : for
            | while"""


def p_for(p):
    """for : FOR for_expression block"""


def p_for_expression(p):
    """for_expression : ID ASSIGN num_term COLON num_term"""


def p_while(p):
    """while : WHILE LPARENT comparison RPARENT block"""


# instrukcję warunkową if-else
def p_branch(p):
    """branch : IF LPARENT comparison RPARENT block %prec IF
              | IF LPARENT comparison RPARENT block ELSE block"""


def p_term(p):
    """term : ID
                | number
                | matrix
                | string"""


def p_num_term(p):
    """num_term : ID
                | number"""


def p_matrix_term(p):
    """matrix_term : ID
                | matrix"""


def p_string_term(p):
    """string_term : ID
                | STRING"""


def p_number(p):
    """number : INT
              | FLOAT"""


def p_string(p):
    """string : STRING"""


# inicjalizację macierzy konkretnymi wartościami
def p_matrix(p):
    """matrix : LSQBRACK matrix_contents RSQBRACK"""


def p_matrix_contents(p):
    """matrix_contents : matrix_contents COMMA matrix_content
                       | matrix_content"""


def p_matrix_content(p):
    """matrix_content : matrix_term
                      | empty"""


def p_expression_term(p):
    """expression : term"""


def p_expression_num_term(p):
    """num_expression : num_term"""


def p_expression_matrix_term(p):
    """matrix_expression : matrix_term"""


def p_expression_string_term(p):
    """string_expression : string_term"""


# wyrażenia binarne, w tym operacje macierzowe 'element po elemencie'
def p_expression_binary(p):
    """expression : num_expression ADD num_expression
                  | num_expression SUB num_expression
                  | num_expression MUL num_expression
                  | num_expression DIV num_expression
                  | matrix_expression DOTADD matrix_expression
                  | matrix_expression DOTSUB matrix_expression
                  | matrix_expression DOTMUL matrix_expression
                  | matrix_expression DOTDIV matrix_expression"""

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
