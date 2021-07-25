#!/usr/bin/env python3.9

# Import ply 
import ply.lex as lex
import ply.yacc as yacc

# Reserved keywords
reserved = {
    'add' : 'ADD',
    'sub' : 'SUB',
    'if' : 'IF'
}

# Define the necessary tokens
tokens = ['IDENTIFIER',
          'INTEGER', 'FLOAT',
          'LPAREN', 'RPAREN',
          ] + list(reserved.values())

# Length of string has priority
# Then order of declaration
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ADD = r'\+'
t_SUB = r'\-'

# Functions have priority over rawstrings
# Order of declaration has priority
def t_IDENTIFIER(t):
   r'[a-zA-Z][a-zA-Z0-9_-]*'
   t.type = reserved.get(t.value)

   if t.type is None:
       t.type = "IDENTIFIER"

   return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Filtering:
# Filter out and track newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

# Discard comments
def t_comment(t):
    r';[^\n]*'
    pass

# Discard unnecessary whitespace
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    pass

# TODO: Add error checking for missing parenthese
def t_eof(t):
    print("EOF")
    return None

# TODO: Global for now
g_lexer = lex.lex()
