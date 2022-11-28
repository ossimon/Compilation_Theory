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


# instrukcje break, continue oraz return i print
def p_call(p):
    """call : BREAK
            | CONTINUE
            | RETURN expression
            | PRINT string"""


def p_matrix_fun(p):
    """matrix_fun : fun_name LPARENT num_expression RPARENT"""


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES"""


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
                   | matrix
                   | number"""


def p_number(p):
    """number : INT
              | FLOAT"""


def p_string(p):
    """string : STRING"""


# inicjalizację macierzy konkretnymi wartościami
def p_matrix(p):
    """matrix : LSQBRACK matrix_contents RSQBRACK
              | matrix_fun"""


def p_matrix_contents(p):
    """matrix_contents : matrix_contents COMMA matrix_content
                       | matrix_content"""


def p_matrix_content(p):
    """matrix_content : matrix_term"""


def p_expression_term(p):
    """expression : term"""


def p_expression(p):
    """expression : term
                  | LPARENT expression RPARENT
                  | num_expression num_binary_operator num_expression
                  | matrix_expression
                  | string_expression"""


# wyrażenia binarne, w tym operacje macierzowe 'element po elemencie'
def p_num_expression_binary(p):
    """num_expression : num_expression num_binary_operator num_expression
                      | LPARENT num_expression RPARENT
                      |
                      | num_expression num_binary_operator num_expression
                      | """


def p_num_binary_operator(p):
    """num_binary_operator : ADD
                           | SUB
                           | MUL
                           | DIV"""


def p_matrix_expression_binary(p):
    """matrix_expression : matrix_expression DOTADD matrix_expression
                         | matrix_expression DOTSUB matrix_expression
                         | matrix_expression DOTMUL matrix_expression
                         | matrix_expression DOTDIV matrix_expression"""


def p_num_binary_operator(p):
    """num_binary_operator : ADD
                           | SUB
                           | MUL
                           | DIV"""


# wyrażenia relacyjne
def p_comparison(p):
    """comparison : num_expression comparison_operator num_expression"""

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
