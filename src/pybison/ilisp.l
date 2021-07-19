%{
// For Yacc compatibility
// bison -d to create a y.tab.h
#include "y.tab.h"

#include <stdio.h>
#include <math.h>

//#define returntoken(tok) /*printf("%d=%s\n", tok, yytext);*/ yylval = PyUnicode_FromString(strdup(yytext)); return (tok);

int line_num = 0;
%}


%option noyywrap

%x COMMENT
%x STRING
%x FUNC						
						
DIGIT [[:digit:]]
ID    [[:alpha:]][[:alnum:]]*

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

\" {
   /* String lexing */
   BEGIN(STRING);
   }

<STRING>.* {
	       printf("String: %s\n", yytext);
           }

<STRING>\" {
           BEGIN(INITIAL);
           }

"(" {
    BEGIN(FUNC);
    return LPAREN
    }

<FUNC>{ID} {
		   BEGIN(INITIAL);
           return OP;
		   }

")" {
    return RPAREN;
}

"+" {
    printf("+\n");
    return ADD;
    }

{ID} {
	 printf("Var: %s\n", yytext);
     }

{DIGIT}+ {
         /* Misceallenous lexing */
         printf( "An integer: %s (%d)\n", yytext,
											 atoi(yytext));
         return NUMBER;
         }

{DIGIT}+"."{DIGIT}* {
                    printf( "A float: %s (%g)\n", yytext,
											      atof(yytext));
                    }

%%

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
