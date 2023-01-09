#!/usr/bin/python

import compiler.scanner as scanner
import ply.yacc as yacc
import compiler.AST as AST
from compiler.TreePrinter import *

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
    i = p[1]
    if isinstance(p[1], str):
        i = AST.Variable(i)
    p[0] = AST.Assign(i, p[2], p[3])


def p_ref(p):
    """ref : ID LSQBRACK num_term RSQBRACK
           | ID LSQBRACK num_term COMMA num_term RSQBRACK"""
    if len(p) == 5:
        p[0] = AST.Ref(AST.Variable(p[1]), p[3])
    else:
        p[0] = AST.Ref(AST.Variable(p[1]), p[3], p[5])


def p_assignment_operator(p):
    """assignment_operator : ASSIGN
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN"""
    if isinstance(p[1], AST.Operator):
        p[0] = p[1]
    else:
        p[0] = AST.Operator(p[1])


def p_expression(p):
    """expression : term
                  | LPARENT expression RPARENT"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_num_expression_binary(p):
    """expression : expression ADD expression
                  | expression SUB expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression"""
    p[0] = AST.BinExpr(p[1], AST.Operator(p[2]), p[3])


def p_expression_negation(p):
    """expression : SUB expression %prec UMINUS"""
    p[0] = AST.UnExpr(p[2], AST.Operator(p[1]))


def p_expression_transpose(p):
    """expression : expression TRANSPOSE"""
    p[0] = AST.UnExpr(p[1], AST.Operator(p[2]))


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
    if isinstance(p[1], AST.Operator):
        p[0] = p[1]
    else:
        p[0] = AST.Operator(p[1])


def p_call1(p):
    """call : BREAK
            | CONTINUE
            | RETURN expression"""
    if len(p) == 2:
        p[0] = AST.SysCall(p[1])
    else:
        p[0] = AST.SysCall(p[1], p[2])


def p_call2(p):
    """call : PRINT print_inputs"""
    p[0] = p[2]


def p_print_inputs1(p):
    """print_inputs : print_inputs COMMA print_input"""
    p[0] = p[1]
    new_input = p[3]
    if not isinstance(new_input, AST.Variable):
        new_input = AST.Variable(new_input)
    p[0].inputs.append(new_input)


def p_print_inputs2(p):
    """print_inputs : print_input"""
    if isinstance(p[1], AST.PrintInputs):
        p[0] = p[1]
    else:
        p[0] = AST.PrintInputs(p[1])


def p_print_input(p):
    """print_input : STRING
                   | ID"""
    if isinstance(p[1], AST.Variable):
        p[0] = p[1]
    else:
        p[0] = AST.Variable(p[1])


def p_matrix_fun(p):
    """matrix_fun : fun_name LPARENT expression RPARENT"""
    p[0] = AST.MatrixFun(p[1], p[3])


def p_fun_name(p):
    """fun_name : EYE
                | ZEROS
                | ONES"""
    if isinstance(p[1], AST.Operator):
        p[0] = p[1]
    else:
        p[0] = AST.Operator(p[1])


def p_loop(p):
    """loop : for
            | while"""
    p[0] = p[1]


def p_for(p):
    """for : FOR for_expression instruction"""
    p[0] = AST.For(p[2], p[3])


def p_for_expression(p):
    """for_expression : ID ASSIGN range"""
    p[0] = AST.ForExpr(AST.Variable(p[1]), p[3])


def p_while(p):
    """while : WHILE LPARENT comparison RPARENT instruction"""
    p[0] = AST.While(p[3], p[5])


def p_branch(p):
    """branch : IF LPARENT comparison RPARENT instruction %prec IFX
              | IF LPARENT comparison RPARENT instruction ELSE instruction"""
    if len(p) == 6:
        p[0] = AST.IfElse(p[3], p[5])
    else:
        p[0] = AST.IfElse(p[3], p[5], p[7])


def p_range(p):
    """range : num_term COLON num_term"""
    p[0] = AST.ForRange(p[1], p[3])


def p_term1(p):
    """term : ID"""
    if isinstance(p[1], AST.Variable):
        p[0] = p[1]
    else:
        p[0] = AST.Variable(p[1])


def p_term2(p):
    """term : number
            | matrix
            | string"""
    p[0] = p[1]


def p_num_term1(p):
    """num_term : ID"""
    if isinstance(p[1], AST.Variable):
        p[0] = p[1]
    else:
        p[0] = AST.Variable(p[1])


def p_num_term2(p):
    """num_term : number"""
    p[0] = p[1]


def p_number1(p):
    """number : INT"""
    if isinstance(p[1], AST.Value):
        p[0] = p[1]
    else:
        p[0] = AST.Value('INT', p[1])


def p_number2(p):
    """number : FLOAT"""
    if isinstance(p[1], AST.Value):
        p[0] = p[1]
    else:
        p[0] = AST.Value('FLOAT', p[1])


def p_string(p):
    """string : STRING"""
    if isinstance(p[1], AST.Value):
        p[0] = p[1]
    else:
        p[0] = AST.Value('STRING', p[1])


def p_matrix1(p):
    """matrix : LSQBRACK vectors RSQBRACK"""
    p[0] = p[2]


def p_matrix2(p):
    """matrix : matrix_fun
              | vector"""
    p[0] = p[1]


def p_vectors1(p):
    """vectors : vectors COMMA vector"""
    p[0] = p[1]
    p[0].vectors.append(p[3])


def p_vectors2(p):
    """vectors : vector"""
    if isinstance(p[1], AST.Matrix):
        p[0] = p[1]
    else:
        p[0] = AST.Matrix(p[1])


def p_vector(p):
    """vector : LSQBRACK vector_contents RSQBRACK"""
    p[0] = p[2]


def p_vector_contents1(p):
    """vector_contents : vector_contents COMMA vector_content"""
    p[0] = p[1]
    # p[0].values.append(p[3])
    p[0].values.append(p[3])


def p_vector_contents2(p):
    """vector_contents : vector_content"""
    if isinstance(p[1], AST.Vector):
        p[0] = p[1]
    else:
        p[0] = AST.Vector(p[1])


def p_vector_content1(p):
    """vector_content : ID"""
    if isinstance(p[1], AST.Variable):
        p[0] = p[1]
    else:
        p[0] = AST.Variable(p[1])


def p_vector_content2(p):
    """vector_content : number"""
    p[0] = p[1]


parser = yacc.yacc()
