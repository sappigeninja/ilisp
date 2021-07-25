%{
#include "lex.yy.c"
%}

%token IDENTIFIER
%token INTEGER FLOAT 

%token LPAREN RPAREN
%token NATIVE FUNC

%start program

%%

program
		:		s_expr program
		;
atom
        :		INTEGER
		|		FLOAT
				;

s_expr
		:		LPAREN NATIVE atom RPAREN
		|		LPAREN NATIVE atom atom RPAREN
				;

%%
