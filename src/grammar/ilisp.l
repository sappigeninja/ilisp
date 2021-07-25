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
