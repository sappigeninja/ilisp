#!/bin/bash

echo "Creating python parser:"
bison2py ilisp.y ilisp.l ilisp.py

echo "Assigning perms:"
sudo chmod +x ilisp.py
