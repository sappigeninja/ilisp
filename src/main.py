#!/usr/bin/env python3.9

# Internal modules
import lexer as l
import parser as p

def main():
    #open text file in read mode
    file = open("../test/main.il", "r")

    for line in file:
        parse = p.g_parser.parse(line)
        print(parse)
    
    pass # End of main

if __name__ == "__main__":
    main()
