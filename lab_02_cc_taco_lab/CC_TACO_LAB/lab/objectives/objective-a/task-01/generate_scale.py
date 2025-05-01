import sys
import copy

prog_prolog = """
#include <stdio.h>
#include <stdlib.h>
#include "instruments.h"
#include "COMPUTE.h"

#ifndef COMPUTE_NAME
#define COMPUTE_NAME baseline
#endif

#ifndef COMPUTE_MODEL_NAME
#define COMPUTE_MODEL_NAME baseline_model
#endif
"""


class BenchedProgram:
    __match_args__ = ("operation_file",)
    def __init__(self,operation_file):
        self.operation_file = operation_file

class ReadOperation:
    __match_args__ = ("file",)
    def __init__(self,file):
        self.file=file


# Statements
class Statement:
    __match_args__ = ("stmt",)
    def __init__(self,stmt):
        self.stmt=stmt

class Function:
    __match_args__ = ("return_type","name","args","body")
    def __init__(self,return_type,name,args,body):
        self.return_type=return_type
        self.name=name
        self.args=args
        self.body=body

class Loop:
    __match_args__ = ("index_var","index_bound","index_increment","body")
    def __init__(self,index_var,index_bound,index_increment,body):
        self.index_var=index_var
        self.index_bound=index_bound
        self.index_increment=index_increment
        self.body=body

class Scale:
    pass

class ScaleModel:
    pass


# Expressions
class Expression:
    __match_args__ = ("expr",)
    def __init__(self,expr):
        self.expr=expr

class ConstAssignment:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class AssignVariable:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Increment:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class LessThan:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Add:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Multiply:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Modulo:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Pointer:
    __match_args__ = ("left","right")
    def __init__(self,left,right):
        self.left=left
        self.right=right

class Array:
    __match_args__ = ("outside","inside")
    def __init__(self,outside,inside):
        self.outside=outside
        self.inside=inside

class Parenthesis:
    __match_args__ = ("body",)
    def __init__(self,body):
        self.body=body

class Constant:
    __match_args__ = ("s",)
    def __init__(self,s):
        self.s=s


class Compile2C():
    def compile2C_expr(self, e):
        match e:
            case ConstAssignment(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"const {l} = {r}"
            case AssignVariable(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} = {r}"
            case Increment(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} += {r}"
            case LessThan(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} < {r}"
            case Add(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} + {r}"
            case Multiply(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} * {r}"
            case Modulo(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l} % {r}"
            case Pointer(l,r):
                l = self.compile2C_expr(l)
                r = self.compile2C_expr(r)
                return f"{l}->{r}"
            case Array(o,i):
                o = self.compile2C_expr(o)
                i = self.compile2C_expr(i)
                return f"{o}[{i}]"
            case Parenthesis(b):
                b = self.compile2C_expr(b)
                return f"({b})"
            case Constant(s):
                return s
            case _:
                raise Exception('compile2C_expr: unexpected ' + repr(s))


    def compile2C_stmt(self, s):
        match s:
            case Expression(expr):
                e = self.compile2C_expr(expr)
                return f"{e};"

            case Function(return_type, name, args, body):
                # Evaluate each part of the function
                return_type = self.compile2C_expr(return_type)
                name = self.compile2C_expr(name)
                args = ", ".join([self.compile2C_expr(expr) for expr in args])

                # Evaluate all statements in body and join them as a string
                body = "\n  ".join([self.compile2C_stmt(stmt) for stmt in body])

                # Combine it all into a C function and return it
                return (
                    f"{return_type} {name} ({args}) {{\n"
                    f"  {body}\n"
                    f"}}\n"
                )

            case Loop(index_var, index_bound, index_increment, body):
                # Build ASTs for each part of the loop
                var_ast = AssignVariable(Constant(f"int {index_var}"), Constant("0"))
                conditional_ast = LessThan(Constant(f"{index_var}"), Constant(f"{index_bound}"))
                increment_ast = Increment(Constant(f"{index_var}"), Constant(f"{index_increment}"))

                # Evaluate each part of the loop
                var_assignment = self.compile2C_stmt(Expression(var_ast))
                conditional = self.compile2C_stmt(Expression(conditional_ast))
                increment = self.compile2C_expr(increment_ast)

                # Evaluate all statements in body and join them as a string
                body = "\n".join([self.compile2C_stmt(stmt) for stmt in body])

                # Combine it all into a C loop and return it
                return (
                    f"for ({var_assignment} {conditional} {increment}) {{\n"
                    f"  {body}\n"
                    f"  }}"
                )

            # TODO Step 1: Create ASTs for the 2 Statements in the COMPUTE_MODEL_NAME function body
            #
            # Go to examples/your_operation/basline.c and create and return ASTs for the 2 Statements
            # in the COMPUTE_MODEL_NAME function.
            # If you want an example take a look at my completed generator in task05.
            case ScaleModel():
                model_flops = Pointer(Constant("model"), Constant("flops"))
                model_bytes = Pointer(Constant("model"), Constant("bytes"))

                op_params = Constant("op_params")
                bytes_value = Pointer(op_params, Constant("m0"))

                # (2 * op_params->m0 + 1) * sizeof(float)
                two_m0 = Multiply(Constant("2"), bytes_value)
                plus_one = Add(two_m0, Constant("1"))

                flops_value = Multiply(plus_one, Constant("sizeof(float)"))
                
                return [
                    Expression(AssignVariable(model_flops, flops_value)),
                    Expression(AssignVariable(model_bytes, bytes_value)),
                ]
            # TODO Step 2: Create a list of ASTs for each Statement in the COMPUTE_NAME function body
            #
            # Go to examples/your_operation/basline.c and create and return a list of ASTs for all the
            # Statements in the COMPUTE_MODEL function.
            # If you want an example take a look at my completed generator in task05.
            case Scale():
                i0 = Constant("i0")
                z_arr_index = Array(Constant("z"), i0)
                x_arr_index = Array(Constant("x"), i0)
                y_arr_index = Array(Constant("y"), Constant("0"))

                expr = Increment(z_arr_index, Multiply(x_arr_index, y_arr_index))

                i0_loop = Loop("i0", "m0", "1", [Expression(expr)])
                return [
                    Expression(ConstAssignment(Constant("int m0"), Pointer(Constant("op_params"), Constant("m0")))),
                    Expression(AssignVariable(Constant("float* x"), Pointer(Constant("inputs"), Constant("x_vect")))),
                    Expression(AssignVariable(Constant("float* y"), Pointer(Constant("inputs"), Constant("y_scalar")))),
                    Expression(AssignVariable(Constant("float* z"), Pointer(Constant("inouts"), Constant("z_vect")))),
                    Expression(Constant("BEGIN_INSTRUMENTATION")),
                    i0_loop,
                    Expression(Constant("END_INSTRUMENTATION")),
                ]

            case _:
                raise Exception('compile2C_stmt: unexpected ' + repr(s))


    def compile2C(self, p):
        match p:
            case Statement(stmt):
                return self.compile2C_stmt(stmt)

            case ReadOperation(file):
                with open(file, 'r') as f:
                    line = f.read().strip()

                operation = None
                operation_model = None
                match line:
                    case "scale":
                        operation = Scale()
                        operation_model = ScaleModel()

                return operation, operation_model

            case BenchedProgram(operation_file):
                operation, operation_model = self.compile2C(ReadOperation(operation_file))
                operation_ast = self.compile2C_stmt(operation)
                operation_model_ast = self.compile2C_stmt(operation_model)

                function_args = [
                    Constant("op_model_t* model"),
                    Constant("op_params_t* op_params"),
                    Constant("op_inputs_t* inputs"),
                    Constant("op_outputs_t* outputs"),
                    Constant("op_inouts_t* inouts"),
                    Constant("hwctx_t* hwctx"),
                ]

                # Create ASTs for the Functions
                return_type = Constant("void")
                model_name = Constant("COMPUTE_MODEL_NAME")
                compute_model = Function(return_type, model_name, function_args, operation_model_ast)

                compute_name = Constant("COMPUTE_NAME")
                compute = Function(return_type, compute_name, function_args[1:], operation_ast)

                # Evaluate ASTs and return the complete C program
                return prog_prolog + "\n" \
                    + self.compile2C_stmt(compute_model) + "\n" \
                    + self.compile2C_stmt(compute)

            case _:
                raise Exception('compile2C: unexpected ' + repr(p))


def main():
    if len(sys.argv) != 3:
        print("Usage: {pn} <outfile> <operation>".format(pn=sys.argv[0]))
        exit(-1)

    out_file = sys.argv[1]
    operation_file = sys.argv[2]

    c = Compile2C()
    p = BenchedProgram(operation_file)
    rs = c.compile2C(p)
    f = open(out_file, "w")
    f.write(rs)
    f.close()


if __name__ == "__main__":
    main()
