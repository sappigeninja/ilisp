#!/usr/bin/env python3.9

# Internal modules
import parser

def main():
    #open text file in read mode
    file = open("../test/main.il", "r")

    #read whole file to a string
    data = file.read()

    parser.g_lexer.input(data)

    # Tokenize
    while True:
        tok = parser.g_lexer.token()
        if not tok:
            break      # No more input
        print(tok)

if __name__ == "__main__":
    main()
