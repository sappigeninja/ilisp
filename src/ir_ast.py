#!/usr/bin/python3.9

import sys

# Define the classes for constructing the AST here
from llvmlite import ir 


# Variable stack
g_variables = {} 

# TODO: Use Atom for error handling / checking
class Atom:
    def __init__(self, t_builder, t_module, t_type, t_value):
        self._builder = t_builder
        self._module = t_module

        self._type = t_type
        self._value = t_value
        pass

    
    def get_type():
        return self._type

    
    def eval(self):
        i = None
        if self._type == "INTEGER":
            i = ir.Constant(ir.IntType(8), int(self._value))
        if self._type == "FLOAT":
            i = ir.Constant(ir.DoubleType(), float(self._value))
        return i

    
# Sexpr:
class Sexpr:
    def __init__(self, t_builder, t_module, t_seq):
        self._builder = t_builder
        self._module = t_module

        self._seq= t_seq
        pass

    
# Arithmetic 
class Addition(Sexpr):
    def eval(self):
        i = self._builder.add(self._seq[0].eval(), self._seq[1]. eval())
        for atom in self._seq[2:]:
            i = self._builder.add(i, atom.eval())
        return i

    
class Subtraction(Sexpr):
    def eval(self):
        i = self._builder.sub(self._seq[0].eval(), self._seq[1]. eval())
        for atom in self._seq[2:]:
            i = self._builder.sub(i, atom.eval())
        return i

    
class Multiplication(Sexpr):
    def eval(self):
        i = self._builder.mul(self._seq[0].eval(), self._seq[1]. eval())
        for atom in self._seq[2:]:
            i = self._builder.mul(i, atom.eval())
        return i

    
class Subtraction(Sexpr):
    def eval(self):
        i = self._builder.sdiv(self._seq[0].eval(), self._seq[1]. eval())
        for atom in self._seq[2:]:
            i = self._builder.sdiv(i, atom.eval())
        return i

    
class If:
    def __init__(self, t_builder, t_module, t_cond, t_sexpr1, t_sexpr2 = None):
        self._builder = t_builder
        self._module = t_module

        self._cond = t_cond
        self._sexpr1 = t_sexpr1
        self._sexpr2 = t_sexpr2
        pass

    
    def eval(self):
        i = None
        if self._sexpr2 is None:
            with self._builder.if_then(self._cond.eval()) as (then):
                with then:
                    i = self._sexpr1.eval()
        else:
            with self._builder.if_else(self._cond.eval()) as (then, otherwise):
                with then:
                    i = self._sexpr1.eval()
                with otherwise:
                    i = self._sexpr2.eval()
        return i


class Conditional:
    def __init__(self, t_builder, t_module, t_seq, t_op = None):
        self._builder = t_builder
        self._module = t_module

        self._seq = t_seq
        self._op = t_op
        pass

    
    def eval(self):
        i = None
        if self._op is None:
            if self._seq is not list:
                i = ir.Constant(ir.IntType(1), int(self._seq))
            else:
                sys.exit("ERROR: No operator was given and a sequence was supplied.")
        return i


# IO:
class Print():
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf

        self.value = value
        pass

        
    def eval(self):
        value = self.value.eval()

        # Declare argument list
        voidptr_ty = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])
        pass
