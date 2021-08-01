#!/usr/bin/env python3.9

# Import ply 
import ply.lex as lex

# TODO: Wrap the lexer and parser in a class

# Define states for more complex parsing
states = (
   ('sexpr', 'inclusive'),
   ('string', 'exclusive')
)

# Reserved keywords
reserved = {
   'add' : 'ADD',
   'sub' : 'SUB',
   'mul' : 'MUL',
   'div' : 'DIV',

   'if' : 'IF',
   'setq' : 'SETQ',
   'print' : 'PRINT'
}

# Define the necessary tokens
tokens = ['IDENTIFIER',
          'INTEGER', 'FLOAT', 'QUOTE', 'STRING',
          'STRING_START', 'STRING_END',
          'LPAREN', 'RPAREN'
          ] + list(reserved.values())

# Length of string has priority
# Then order of declaration
t_INITIAL_IDENTIFIER  = r'[a-zA-Z][a-zA-Z0-9_-]*'

t_QUOTE = r'\''

# Natives and literals
t_sexpr_ADD = r'\+'
t_sexpr_SUB = r'\-'
t_sexpr_MUL = r'\*'
t_sexpr_DIV = r'\/'

# Functions have priority over rawstrings
# Order of declaration has priority
def t_sexpr_IDENTIFIER(t):
   r'[a-zA-Z][a-zA-Z0-9_-]*'
   type = reserved.get(t.value)

   if type is not None:
       t.type = type

   return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String lexing:
def t_string_STRING(t):
   r'[^\"]+'
   return t

def t_STRING_START(t):
   r'\"'
   t.lexer.push_state('string')
   pass

def t_string_STRING_END(t):
   r'\"'
   t.lexer.pop_state()
   pass

# S-expression lexing:
def t_LPAREN(t):
   r'\('
   t.lexer.push_state('sexpr')
   return t

def t_sexpr_RPAREN(t):
   r'\)'
   t.lexer.pop_state()
   return t

# Filtering:
# Filter out and track newlines
def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

# Discard comments
def t_comment(t):
    r';[^\n]*'
    pass

# Remove spaces in every state
def t_space(t):
   r'\s'
   pass

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    pass

def t_sexpr_error(t):
   pass

def t_string_error(t):
   pass

# EOF handling:
def t_eof(t):
   # TODO: Add EOF handling here
   pass

def t_sexpr_eof(t):
   print("EOF was reached and there is no closing parenthesis")
   pass

def t_string_eof(t):
   print("EOF was reached and there is no closing \"")
   pass

# Return the above defined lexer
def get_lexer():
   return lex.lex()
