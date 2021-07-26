#!/usr/bin/env python3.9

from lexer import tokens
import ply.yacc as yacc

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
    print("Statement: ", p[0])
    pass

# Sexpression grammars:
def p_sexpr_seq(p):
    'sexpr : seq'
    p[0] = p[1]
    pass

# TODO: Implement functions
def p_sexpr_function(p):
    'sexpr : LPAREN IDENTIFIER RPAREN'
    pass

def p_sexpr_function_args(p):
    'sexpr : LPAREN IDENTIFIER sexpr RPAREN'
    pass

def p_sexpr_addition(p):
    'sexpr : LPAREN ADD sexpr RPAREN'
    p[0] = p[3][0]
    for atom in p[3][1:]:
        p[0] += atom

    pass

def p_sexpr_subtraction(p):
    'sexpr : LPAREN SUB sexpr RPAREN'
    p[0] = p[3][0]
    for atom in p[3][1:]:
        p[0] -= atom

# Sequence grammars:
def p_seq(p):
    'seq : atom'
    p[0] = p[1]
    pass

def p_seq_recursive(p):
    'seq : atom seq'
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
    p[0] = p[1]

    print("INT: ", p[1])
    pass

def p_atom_float(p):
    'atom : FLOAT'
    p[0] = p[1]

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
    print(f"Syntax error! {p.value!r}")
    pass

g_parser = yacc.yacc()
