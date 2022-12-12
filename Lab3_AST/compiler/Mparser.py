#!/usr/bin/python

import compiler.scanner as scanner
import ply.yacc as yacc
import numpy as np

tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'SMALLER', 'LARGER', 'SMALLEREQ', 'LARGEREQ', 'NOTEQ', 'EQ'),
    ('left', 'ADD', 'SUB', 'DOTADD', 'DOTSUB'),
    ('left', 'MUL', 'DIV', 'DOTMUL', 'DOTDIV'),
    ('left', 'UMINUS'),
    ('left', 'TRANSPOSE')
)

start = 'program'


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions"""


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction"""


def p_instruction(p):
    """instruction : assignment SEMICOLON
                   | call SEMICOLON
                   | loop
                   | branch
                   | LCURLBRACK instructions RCURLBRACK"""


def p_assignment(p):
    """assignment : ID assignment_operator expression
                  | ID matrix assignment_operator expression"""


def p_assignment_operator(p):
    """assignment_operator : ASSIGN
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""


def p_expression(p):
    """expression : term
                  | LPARENT expression RPARENT"""


def p_num_expression_binary(p):
    """expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""


def p_expression_negation(p):
    """expression : SUB expression %prec UMINUS"""


def p_expression_transpose(p):
    """expression : expression TRANSPOSE"""


def p_comparison(p):
    """comparison : expression comparison_operator expression"""


def p_comparison_operator(p):
    """comparison_operator : SMALLER
                          | LARGER
                          | SMALLEREQ
                          | LARGEREQ
                          | NOTEQ
                          | EQ"""


def p_call(p):
    """call : BREAK
            | CONTINUE
            | RETURN expression
            | PRINT print_inputs"""


def p_print_inputs(p):
    """print_inputs : print_inputs COMMA print_input
                    | print_input"""


def p_print_input(p):
    """print_input : STRING
                   | ID"""


def p_matrix_fun(p):
    """matrix_fun : fun_name LPARENT expression RPARENT"""


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES"""


def p_loop(p):
    """loop : for
            | while"""


def p_for(p):
    """for : FOR for_expression instruction"""


def p_for_expression(p):
    """for_expression : ID ASSIGN range"""


def p_while(p):
    """while : WHILE LPARENT comparison RPARENT instruction"""


def p_branch(p):
    """branch : IF LPARENT comparison RPARENT instruction %prec IFX
              | IF LPARENT comparison RPARENT instruction ELSE instruction"""


def p_range(p):
    """range : num_term COLON num_term"""


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


def p_matrix(p):
    """matrix : LSQBRACK matrix_contents RSQBRACK
              | matrix_fun"""


def p_matrix_contents(p):
    """matrix_contents : matrix_contents COMMA matrix_content
                       | matrix_content"""


def p_matrix_content(p):
    """matrix_content : matrix_term"""


parser = yacc.yacc()
