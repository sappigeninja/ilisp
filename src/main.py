#!/usr/bin/env python3.9

# Packages
import bison

# Tell python to search for modules in subdirs
import os
import sys
for entry in os.listdir():
    if os.path.isdir(entry):
        sys.path.insert(0, entry)

# Internal modules
import ilisp

def main():
    print("Hello World!")
    parser = ilisp.Parser()
    parser.run()

if __name__ == "__main__":
    main()
