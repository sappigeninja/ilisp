%{

%}

%token IDENTIFIER
%token NUMBER
%token OP
%token LPAREN RPAREN					 

%start translation_unit
%%

s_expr:
		|		LPAREN OP NUMBER RPAREN
		|		RPAREN OP s_expr RPAREN

%%
