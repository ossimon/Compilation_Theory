#!/usr/bin/python

import compiler.scanner as scanner
import ply.yacc as yacc
import compiler.AST as AST

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

    p[0] = AST.Program(p[1])


def p_instructions_1(p):
    """instructions : instructions instruction"""
    p[0] = p[1]
    p[0].instructions.append(p[2])


def p_instructions_2(p):
    """instructions : instruction"""
    if isinstance(p[1], AST.Instructions):
        p[0] = p[1]
    else:
        p[0] = AST.Instructions(p[1])


def p_instruction(p):
    """instruction : assignment SEMICOLON
                   | call SEMICOLON
                   | loop
                   | branch
                   | LCURLBRACK instructions RCURLBRACK"""
    if len(p) < 4:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_assignment(p):
    """assignment : ID assignment_operator expression
                  | ref assignment_operator expression"""
    p[0] = AST.Assign(p[1], p[2], p[3])


def p_ref(p):
    """ref : ID LSQBRACK num_term RSQBRACK
           | ID LSQBRACK num_term COMMA num_term RSQBRACK"""
    if len(p) == 5:
        p[0] = AST.Ref(p[3])
    else:
        p[0] = AST.Ref(p[3], p[5])


def p_assignment_operator(p):
    """assignment_operator : ASSIGN
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""
    p[0] = p[1]


def p_expression(p):
    """expression : term
                  | LPARENT expression RPARENT"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_num_expression_binary(p):
    """expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = AST.BinExpr(p[1], p[2], p[3])


def p_expression_negation(p):
    """expression : SUB expression %prec UMINUS"""
    p[0] = AST.UnExpr(p[2], p[1])


def p_expression_transpose(p):
    """expression : expression TRANSPOSE"""
    p[0] = AST.UnExpr(p[1], p[2])


def p_comparison(p):
    """comparison : expression comparison_operator expression"""
    p[0] = AST.CompOp(p[1], p[2], p[3])


def p_comparison_operator(p):
    """comparison_operator : SMALLER
                          | LARGER
                          | SMALLEREQ
                          | LARGEREQ
                          | NOTEQ
                          | EQ"""
    p[0] = p[1]


def p_call(p):
    """call : BREAK
            | CONTINUE
            | RETURN expression
            | PRINT print_inputs"""
    if len(p) == 2:
        p[0] = AST.SysCall(p[1])
    else:
        p[0] = AST.SysCall(p[1], p[2])


def p_print_inputs1(p):
    """print_inputs : print_inputs COMMA print_input"""
    p[0] = p[1]
    p[0].inputs.append(p[2])


def p_print_inputs2(p):
    """print_inputs : print_input"""
    if isinstance(p[1], AST.PrintInputs):
        p[0] = p[1]
    else:
        p[0] = AST.PrintInputs(p[1])


def p_print_input(p):
    """print_input : STRING
                   | ID"""
    p[0] = p[1]


def p_matrix_fun(p):
    """matrix_fun : fun_name LPARENT expression RPARENT"""
    p[0] = AST.MatrixFun(p[1], p[3])


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES"""
    p[0] = p[1]


def p_loop(p):
    """loop : for
            | while"""
    p[0] = p[1]


def p_for(p):
    """for : FOR for_expression instruction"""
    p[0] = AST.For(p[2], p[3])


def p_for_expression(p):
    """for_expression : ID ASSIGN range"""
    p[0] = AST.ForExpr(p[1], p[3])


def p_while(p):
    """while : WHILE LPARENT comparison RPARENT instruction"""
    p[0] = AST.While(p[3], p[5])


def p_branch(p):
    """branch : IF LPARENT comparison RPARENT instruction %prec IFX
              | IF LPARENT comparison RPARENT instruction ELSE instruction"""


def p_range(p):
    """range : num_term COLON num_term"""
    p[0] = AST.ForRange(p[1], p[3])


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
