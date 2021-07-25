%{
#include "lex.yy.c"
%}

%token IDENTIFIER
%token INTEGER FLOAT 

%token LPAREN RPAREN
%token NATIVE FUNC

%start program

%%

program:		/* empty */
		|		s-expr program
		;
atom: 			INTEGER
		|		FLOAT
				;

s-expr:			atom
		|		LPAREN NATIVE s-expr RPAREN
		|		LPAREN NATIVE s-expr s-expr RPAREN
				;

%%
