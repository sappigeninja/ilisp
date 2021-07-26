#!/usr/bin/env python3.9

# Internal modules
import lexer as l
import parser as p

def main():
    #open text file in read mode
    file = open("../test/main.il", "r")

    #read whole file to a string
    data = file.read()

    l.g_lexer.input(data)

    # Tokenize
    while True:
        tok = l.g_lexer.token()
        if not tok:
            break      # No more input
        print(tok)

    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        parse = p.g_parser.parse(s)
        print(parse)

    pass # End of main

if __name__ == "__main__":
    main()
