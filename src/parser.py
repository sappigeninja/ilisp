#!/usr/bin/env python3.9

from lexer import tokens

import ply.yacc as yacc
import ir_ast as ast

# These are assigned in main
g_module = None
g_builder = None
g_printf = None

# Important start at the statement not the empty
start = 'statement'

def p_empty(p):
    'empty :'
    pass

def p_statement_empty(p):
    'statement : empty'
    pass

def p_statement_sexpr(p):
    'statement : sexpr'
    p[0] = p[1]
    p[0].eval()
    pass

# Sexpression grammars:
def p_sexpr_function(p):
    'sexpr : LPAREN IDENTIFIER RPAREN'
    pass

def p_sexpr_function_args(p):
    'sexpr : LPAREN IDENTIFIER seq RPAREN'
    pass

def p_sexpr_addition(p):
    'sexpr : LPAREN ADD seq RPAREN'
    p[0] = ast.Addition(g_builder, g_module, p[3])
    pass

def p_sexpr_subtraction(p):
    'sexpr : LPAREN SUB seq RPAREN'
    p[0] = ast.Subtraction(g_builder, g_module, p[3])
    pass

def p_sexpr_multiplication(p):
    'sexpr : LPAREN MUL seq RPAREN'
    p[0] = ast.Multiplication(g_builder, g_module, p[3])
    pass

def p_sexpr_division(p):
    'sexpr : LPAREN DIV seq RPAREN'
    p[0] = ast.Division(g_builder, g_module, p[3])
    pass

# TODO: If statements should also have atoms
def p_sexpr_if(p):
    'sexpr : LPAREN IF cond sexpr RPAREN'
    p[0] = ast.If(g_builder, g_module, p[3], p[4])
    pass

def p_sexpr_if_else(p):
    'sexpr : LPAREN IF cond sexpr sexpr RPAREN'
    p[0] = ast.If(g_builder, g_module, p[3], p[4], p[5])
    pass

# Printing:
def p_sexpr_print(p):
    'sexpr : LPAREN PRINT seq RPAREN'
    p[0] = ast.Print(g_builder, g_module, g_printf, p[3])
    pass

# Sequence grammars:
# Also take care of empty sequences
def p_seq_empty(p):
    'seq : empty'
    p[0] = None
    pass

def p_seq(p):
    '''seq : atom
           | sexpr'''
    p[0] = p[1]
    pass

def p_seq_recursive(p):
    '''seq : atom seq
           | sexpr seq'''
    # Store the sequence properly as a list
    p[0] = [p[1]]
    if type(p[2]) is list:
        for atom in p[2]:
            p[0].append(atom)
    else:
        p[0].append(p[2])
    pass

# Atom grammars:
def p_atom_integer(p):
    'atom : INTEGER'
    p[0] = ast.Atom(g_builder, g_module, "INTEGER", p[1])

    print("INT: ", p[1])
    pass

def p_atom_float(p):
    'atom : FLOAT'
    p[0] = ast.Atom(g_builder, g_module, "FLOAT", p[1])

    print("FLOAT: ", p[1])
    pass

# TODO: Add lists later

def p_atom_STRING(p):
    'atom : STRING'
    p[0] = p[1]

    print("STR: ", p[1])
    pass

def p_atom_identifier(p):
    'atom : IDENTIFIER'
    p[0] = p[1]

    print("ID: ", p[1])
    pass

# Error handling
def p_error(p):
    print("Error: ", end="")
    if p is None:
        print("Incomplete expression EOF reached!")
    else:
        print(f"Syntax error! {p.value!r}")
        print(f"Line no: {p.lineno}")
    pass

# Return the above defined parser
def get_parser():
    return yacc.yacc()
