#!/usr/bin/env python3.9

# Internal modules
import lexer as l
import parser as p
import codegen as cg

def main():
    # TODO: Ugly code find a more clean way of doing this
    # Must be set before use of the parser
    codegen = cg.CodeGen()
    p.g_module = codegen.module
    p.g_builder = codegen.builder
    p.g_printf = codegen.printf

    # Create the lexer and parser
    lexer = l.get_lexer()
    parser = p.get_parser()

    #open text file in read mode
    file = open("../test/main.il", "r")
    for line in file:
        parse = parser.parse(line)
        print(parse)

    # Create an LLVM IR code file
    # generate assembly with $ llc output.ll
    # Run it with $ lli output.ll
    codegen.create_ir()
    codegen.save_ir("output.ll")
    pass # End of main

if __name__ == "__main__":
    main()
