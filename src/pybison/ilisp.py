#!/usr/bin/env python

"""
PyBison file automatically generated from grammar file ilisp.y
You can edit this module, or import it and subclass the Parser class
"""

import sys

from bison import BisonParser, BisonNode, BisonSyntaxError

bisonFile = 'ilisp.y'  # original bison file
lexFile = 'ilisp.l'    # original flex file


class Parser(BisonParser):
    """
    bison Parser class generated automatically by bison2py from the
    grammar file "ilisp.y" and lex file "ilisp.l"

    You may (and probably should) edit the methods in this class.
    You can freely edit the rules (in the method docstrings), the
    tokens list, the start symbol, and the precedences.

    Each time this class is instantiated, a hashing technique in the
    base class detects if you have altered any of the rules. If any
    changes are detected, a new dynamic lib for the parser engine
    will be generated automatically.
    """

    # -------------------------------------------------
    # Default class to use for creating new parse nodes
    # -------------------------------------------------
    defaultNodeClass = BisonNode

    # --------------------------------------------
    # basename of binary parser engine dynamic lib
    # --------------------------------------------
    bisonEngineLibName = 'ilisp-engine'

    # ----------------------------------------------------------------
    # lexer tokens - these must match those in your lex script (below)
    # ----------------------------------------------------------------
    tokens = ['IDENTIFIER', 'INTEGER', 'FLOAT', 'LPAREN', 'RPAREN', 'NATIVE', 'FUNC']

    # ------------------------------
    # precedences
    # ------------------------------
    precedences = (
        )

    # ---------------------------------------------------------------
    # Declare the start target here (by name)
    # ---------------------------------------------------------------
    start = 'program'

    # ---------------------------------------------------------------
    # These methods are the python handlers for the bison targets.
    # (which get called by the bison code each time the corresponding
    # parse target is unambiguously reached)
    #
    # WARNING - don't touch the method docstrings unless you know what
    # you are doing - they are in bison rule syntax, and are passed
    # verbatim to bison to build the parser engine library.
    # ---------------------------------------------------------------

    def on_progra(self, target, option, names, values):
        """
        progra
            : /* empty */
            | s-expr program
        """
        return self.defaultNodeClass(
            target='progra',
            option=option,
            names=names,
            values=values)

    def on_ato(self, target, option, names, values):
        """
        ato
            : INTEGER
            | FLOAT
        """
        return self.defaultNodeClass(
            target='ato',
            option=option,
            names=names,
            values=values)

    def on_s-exp(self, target, option, names, values):
        """
        s-exp
            : atom
            | LPAREN NATIVE s-expr RPAREN
            | LPAREN NATIVE s-expr s-expr RPAREN
        """
        return self.defaultNodeClass(
            target='s-exp',
            option=option,
            names=names,
            values=values)

    # -----------------------------------------
    # raw lex script, verbatim here
    # -----------------------------------------
    lexscript = r"""
%{
// For Yacc compatibility
// bison -d to create a y.tab.h
#include "ilisp.tab.h"

// Necessary for pybison
#include <stdio.h>
#include <string.h>
#include "Python.h"
#define YYSTYPE void *
#include "tokens.h"
extern void *py_parser;
extern void (*py_input)(PyObject *parser, char *buf, int *result, int max_size);
#define returntoken(tok) yylval = PyString_FromString(strdup(yytext)); return (tok);
#define YY_INPUT(buf,result,max_size) {(*py_input)(py_parser, buf, &result, max_size);}

// Necessary for atoi
#include <math.h>

int line_num = 0;
%}

%option noyywrap

%x COMMENT
%x STRING
%x OPERATION

DIGIT [[:digit:]]
ID    [[:alpha:]][[:alnum:]]*

NATIVE "+"|"-"
						
%%

";" {
    /* Comment lexing */
    BEGIN(COMMENT);
}

<COMMENT>.* {
	printf("Comment: %s\n", yytext);
}

<COMMENT>\n {
    BEGIN(INITIAL);
    line_num++;
}

\"
    {
    /* String lexing */
    BEGIN(STRING);
}

<STRING>[^\"]* {
	printf("String: %s\n", yytext);
}

<STRING>\" {
   BEGIN(INITIAL);
}

"(" {
    BEGIN(OPERATION);
    returntoken(LPAREN);
}

<OPERATION>{NATIVE} {
   BEGIN(INITIAL);
   printf("NATIVE operation: %s\n", yytext);
   returntoken(NATIVE);
}

<OPERATION>{ID} {
	BEGIN(INITIAL);
    printf("FUNC operation: %s\n", yytext);
    returntoken(FUNC);
}

")" {
    returntoken(RPAREN);
}

{ID} {
    /* Misceallenous lexing */
	printf("Var: %s\n", yytext);
    }

{DIGIT}+ {
    printf( "An integer: %s (%d)\n", yytext,
									 atoi(yytext));
    returntoken(INTEGER);
}

{DIGIT}+"."{DIGIT}* {
    printf( "A float: %s (%g)\n", yytext,
							      atof(yytext));
    returntoken(FLOAT);
}

%%

// Necessary for pybison
yywrap()
{
	return(1);
}

/*
// TODO: Fix this flex says its defined multiple times
int main(argc, argv)
int argc;
char **argv;
{
    ++argv, --argc;
    if ( argc > 0 )
            yyin = fopen( argv[0], "r" );
    else
            yyin = stdin;

    yylex();
}
*/

    """
    # -----------------------------------------
    # end raw lex script
    # -----------------------------------------


def usage():
    print('%s: PyBison parser derived from %s and %s' % (sys.argv[0], bisonFile, lexFile))
    print('Usage: %s [-k] [-v] [-d] [filename]' % sys.argv[0])
    print('  -k       Keep temporary files used in building parse engine lib')
    print('  -v       Enable verbose messages while parser is running')
    print('  -d       Enable garrulous debug messages from parser engine')
    print('  filename path of a file to parse, defaults to stdin')


def main(*args):
    """
    Unit-testing func
    """

    keepfiles = 0
    verbose = 0
    debug = 0
    filename = None

    for s in ['-h', '-help', '--h', '--help', '-?']:
        if s in args:
            usage()
            sys.exit(0)

    if len(args) > 0:
        if '-k' in args:
            keepfiles = 1
            args.remove('-k')
        if '-v' in args:
            verbose = 1
            args.remove('-v')
        if '-d' in args:
            debug = 1
            args.remove('-d')
    if len(args) > 0:
        filename = args[0]

    p = Parser(verbose=verbose, keepfiles=keepfiles)
    tree = p.run(file=filename, debug=debug)
    return tree


if __name__ == '__main__':
    main(*(sys.argv[1:]))

