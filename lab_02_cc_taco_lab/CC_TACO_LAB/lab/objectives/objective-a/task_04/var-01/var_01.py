#!/bin/env python3
import sys
from ast import *
from typing import List
from enum import IntEnum
import copy

# Just print these directly, the schedule does not change these and so we don't need
# AST representation
template_defines = """
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

# NOTE: Probably don't even need a class, no state stored anyways
# But we might as well follow how the textbook suggests
class Gen_Code:
    def gencode_exp(self, e, env) -> str:
        match e:
            case UnaryOp(UAdd(), value):
                value_gen = self.gencode_exp(value, env)
                return f"(++{value_gen})"
            case UnaryOp(USub(), value):
                value_gen = self.gencode_exp(value, env)
                return f"(-{value_gen})"
            case BinOp(left, Add(), right):
                l = self.gencode_exp(left, env)
                r = self.gencode_exp(right, env)
                return f"({l} + {r})"
            case BinOp(left, Sub(), right):
                l = self.gencode_exp(left, env)
                r = self.gencode_exp(right, env)
                return f"({l} - {r})"
            case BinOp(left, Mod(), right):
                l = self.gencode_exp(left, env)
                r = self.gencode_exp(right, env)
                return f"({l} % {r})"
            case BinOp(left, Mult(), right):
                l = self.gencode_exp(left, env)
                r = self.gencode_exp(right, env)
                return f"({l} * {r})"
            case Constant(value):
                return f"{value}"
            case Name(id):
                return f"{id}"

            case Subscript(value=value, slice=slice, ctx=ctx):
                value_gen = self.gencode_exp(value, env)
                slice_gen = self.gencode_exp(slice, env)
                return f"{value_gen}[{slice_gen}]"
            case Call(func=func, args=args, keywords=keywords):
                func_gen = self.gencode_exp(func, env)
                args_gen = [self.gencode_exp(arg, env) for arg in args]
                args_string = ", ".join(args_gen)
                return f"{func_gen}({args_string})"
            case Attribute(value=value, attr=attr, ctx=ctx):
                value_gen = self.gencode_exp(value, env)
                return f"{value_gen}->{attr}"
            case _:
                raise Exception("error in interp_stmt, unexpected " + repr(e))

    def gencode_stmt(self, s, env, cont) -> str:
        match s:
            case Expr(value):
                self.gencode_exp(value, env)
                return self.gencode_stmts(cont, env)

            case Assign(targets=targets, value=value):
                # Handle multiple targets
                if len(targets) == 1:
                    target_gen = self.gencode_exp(targets[0], env)
                    value_gen = self.gencode_exp(value, env)
                    return f"{target_gen} = {value_gen};\n" + self.gencode_stmts(cont, env)
                else:
                    # Multiple targets case
                    value_gen = self.gencode_exp(value, env)
                    result = ""
                    for target in targets:
                        target_gen = self.gencode_exp(target, env)
                        result += f"{target_gen} = {value_gen};\n"
                    return result + self.gencode_stmts(cont, env)

            # For C variable declarations, can pass the type
            case AnnAssign(target=id, annotation=type_name, value=value):
                type_gen = self.gencode_exp(type_name, env)
                name_gen = self.gencode_exp(id, env)

                # Has an initial value
                if value:
                    value_gen = self.gencode_exp(value, env)
                    return f"{type_gen} {name_gen} = {value_gen};\n" + self.gencode_stmts(cont, env)
                    # No initial value
                else:
                    return f"{type_gen} {name_gen};\n" + self.gencode_stmts(cont, env)

            # We sneak in the range and the increment amount, assumes pre-declaration of variables
            case For(target=id, iter=Call(args=[start, end, increment]), body=body):
                name_gen = self.gencode_exp(id, env)
                start_gen = self.gencode_exp(start, env)
                end_gen = self.gencode_exp(end, env)
                increment_gen = self.gencode_exp(increment, env)
                body_gen = self.gencode_stmts(body, env)

                return (
                    f"for ({name_gen} = {start_gen}; {name_gen} < {end_gen}; {name_gen} += {increment_gen})\n" +
                        "{\n" +
                        f"{body_gen}\n" +
                        "}\n" +
                        self.gencode_stmts(cont, env)
                )

            case FunctionDef(name=name, args=args, body=body, returns=returns):
                return_gen = self.gencode_exp(returns, env)
                name_gen = self.gencode_exp(name, env)

                args_gen = []
                for arg in args.args:
                    arg_type = self.gencode_exp(arg.annotation, env)
                    arg_name = self.gencode_exp(arg.arg, env)
                    args_gen.append(f"{arg_type} {arg_name}")

                args_string = ", ".join(args_gen)

                body_gen = self.gencode_stmts(body, env)

                return (
                    f"{return_gen} {name_gen}({args_string})\n" +
                    "{\n" +
                    f"{body_gen}\n" +
                    "}\n" +
                    self.gencode_stmts(cont,env)
                )

            case _:
                raise Exception("error in interp_stmt, unexpected " + repr(s))

    def gencode_stmts(self, ss, env) -> str:
        match ss:
            case []:
                return ""

            case [s, *ss]:
                return self.gencode_stmt(s, env, ss)

            case _:
                raise Exception("error in interp_stmts, unexpected " + repr(ss))

    def gencode(self, p):
        match p:
            case Module(body):
                return self.gencode_stmts(body, {})

            case _:
                raise Exception("error in interp, unexpected " + repr(p))

def generate_outer_product_AST() -> Module:
     # Create the main function body
    body = [
        # Variable declarations
        AnnAssign(
            target=Name('m0'),
            annotation=Name('const int'),
            value=Name('op_params->m0'),
            simple=1
        ),
        AnnAssign(
            target=Name('n0'),
            annotation=Name('const int'),
            value=Name('op_params->n0'),
            simple=1
        ),
        AnnAssign(
            target=Name('rs_c'),
            annotation=Name('const int'),
            value=Name('op_params->rs_c'),
            simple=1
        ),
        AnnAssign(
            target=Name('cs_c'),
            annotation=Name('const int'),
            value=Name('op_params->cs_c'),
            simple=1
        ),
        AnnAssign(
            target=Name('x'),
            annotation=Name('float *'),
            value=Name('inputs->x_vect'),
            simple=1
        ),
        AnnAssign(
            target=Name('y'),
            annotation=Name('float *'),
            value=Name('inputs->y_vect'),
            simple=1
        ),
        AnnAssign(
            target=Name('C'),
            annotation=Name('float *'),
            value=Name('inouts->C_mat'),
            simple=1
        ),
        AnnAssign(
            target=Name('i0'),
            annotation=Name('int'),
            simple=1
        ),
        AnnAssign(
            target=Name('j0'),
            annotation=Name('int'),
            simple=1
        ),
        # Nested loops for outer product
        For(
            target=Name('i0'),
            iter=Call(
                func=Name('n/a'),
                args=[Constant(0), Name('m0'), Constant(1)],
                keywords=[]
            ),
            body=[
                For(
                    target=Name('j0'),
                    iter=Call(
                        func=Name('n/a'),
                        args=[Constant(0), Name('n0'), Constant(1)],
                        keywords=[]
                    ),
                    body=[
                        AnnAssign(
                            target=Name(''),
                            annotation=Name('BEGIN_INSTRUMENTATION'),
                            simple=1
                        ),
                        Assign(
                            targets=[Subscript(
                                value=Name('C'),
                                slice=BinOp(
                                    BinOp(
                                        Name('i0'),
                                        Mult(),
                                        Name('rs_c')
                                    ),
                                    Add(),
                                    BinOp(
                                        Name('j0'),
                                        Mult(),
                                        Name('cs_c')
                                    )
                                ),
                                ctx=Store()
                            )],
                            value=BinOp(
                                Subscript(
                                    value=Name('C'),
                                    slice=BinOp(
                                        BinOp(
                                            Name('i0'),
                                            Mult(),
                                            Name('rs_c')
                                        ),
                                        Add(),
                                        BinOp(
                                            Name('j0'),
                                            Mult(),
                                            Name('cs_c')
                                        )
                                    ),
                                    ctx=Load()
                                ),
                                Add(),
                                BinOp(
                                    Subscript(
                                        value=Name('x'),
                                        slice=Name('i0'),
                                        ctx=Load()
                                    ),
                                    Mult(),
                                    Subscript(
                                        value=Name('y'),
                                        slice=Name('j0'),
                                        ctx=Load()
                                    )
                                )
                            )
                        ),
                        AnnAssign(
                            target=Name(''),
                            annotation=Name('END_INSTRUMENTATION'),
                            simple=1
                        )
                    ]
                )
            ]
        ),

    ]
    
    # Create the main function
    main_function = FunctionDef(
        name=Name("COMPUTE_NAME"),
        args=arguments(
            args=[
                arg(arg=Name('*op_params'), annotation=Name("op_params_t")),
                arg(arg=Name('*inputs'), annotation=Name("op_inputs_t")),
                arg(arg=Name('*outputs'), annotation=Name("op_outputs_t")),
                arg(arg=Name('*inouts'), annotation=Name("op_inouts_t")),
                arg(arg=Name('*hwctx'), annotation=Name("hwctx_t")),
            ],
        ),
        body=body,
        returns=Name("void")
    )
    
    # Create the model function
    model_function = FunctionDef(
        name=Name("COMPUTE_MODEL_NAME"),
        args=arguments(
            args=[
                arg(arg=Name('*model'), annotation=Name("op_model_t")),
                arg(arg=Name('*op_params'), annotation=Name("op_params_t")),
                arg(arg=Name('*op_inputs'), annotation=Name("op_inputs_t")),
                arg(arg=Name('*op_outputs'), annotation=Name("op_outputs_t")),
                arg(arg=Name('*op_inouts'), annotation=Name("op_inouts_t")),
                arg(arg=Name('*hwctx'), annotation=Name("hwctx_t")),
            ],
        ),
        body=[
            Assign(
                targets=[Attribute(
                    value=Name('model'),
                    attr='flops',
                    ctx=Store()
                )],
                value=BinOp(
                    BinOp(
                        Constant(2),
                        Mult(),
                        Name('op_params->m0')
                    ),
                    Mult(),
                    Name('op_params->n0')
                )
            ),
            Assign(
                targets=[Attribute(
                    value=Name('model'),
                    attr='bytes',
                    ctx=Store()
                )],
                value=BinOp(
                    BinOp(
                        BinOp(
                            BinOp(
                                BinOp(
                                    Constant(2),
                                    Mult(),
                                    BinOp(
                                        Name('op_params->m0'),
                                        Mult(),
                                        Name('op_params->n0')
                                    )
                                ),
                                Add(),
                                Name('op_params->m0')
                            ),
                            Add(),
                            Name('op_params->n0')
                        ),
                        Mult(),
                        Call(
                            func=Name('sizeof'),
                            args=[Name('float')],
                            keywords=[]
                        )
                    ),
                    Mult(),
                    Constant(1)
                )
            )
        ],
        returns=Name("void")
    )
    
    # Create the module
    module = Module(
        body=[
            model_function,
            main_function
        ]
    )
    
    return module

def operation_to_AST(filename: str) -> Module:
    """
    Convert an operation file to an AST representing an outer product computation.
    
    Args:
        filename: Path to the operation file
        
    Returns:
        Module: AST representation of the outer product computation
    """
    module = None
    # Read dimensions from the first line
    with open(filename, 'r') as file:
        file_lines = file.readlines()
       
    print(file_lines)
    operation = file_lines[0].strip().split()
    print(operation)
   
    match operation:
        case ['outerproduct']:
            module = generate_outer_product_AST()
            return module
    
    return module
   
    
   

class Schedule_Type(IntEnum):
    UNKOWN = -1
    UNROLL = 0
    INTERCHANGE = 1
    SPLIT = 2

# Returns the unrolled list of statements, is recursive, because by unrolling other loops you may duplicate
# nested loops
def do_unroll(module: Module, loop_name: str):
    # Find the function we want to apply the schedule on and the constant row, col count
    operation_func: FunctionDef = None
    counts = {
        "(R)" : 0,
        "(Q)" : 0,
    }
    for node in module.body:
        if isinstance(node, AnnAssign):
            if node.target.id == 'R':
                counts["(R)"] = node.value
            elif node.target.id == 'Q':
                counts["(Q)"] = node.value

        if isinstance(node, FunctionDef):
            operation_func = node
    assert(operation_func != None and counts["(Q)"] != 0 and counts["(R)"] != 0)

    # Find first loop
    loop: For = None
    parent_body_idx = 0
    for parent_body_idx, node in enumerate(operation_func.body):
        if isinstance(node, For):
            loop = node
            break

    assert(loop != None)


    # Grab the loop to unroll
    previous = None # For checking if we can't find the loop to unroll
    parent = operation_func
    while loop.target.id != loop_name:

        # No infinite loops if we have are looking for an already unrolled loop
        if loop == previous:
            break
        previous = loop

        for parent_body_idx, node in enumerate(loop.body):
            if isinstance(node, For):
                parent = loop
                loop = node
                break # Just the first for loop we find

    if loop.target.id != loop_name:
        return

    iter: Call = loop.iter
    # Can either be a name or constant
    start = iter.args[0].value if isinstance(iter.args[0], Constant) else counts[iter.args[0].id].value
    end   = iter.args[1].value if isinstance(iter.args[1], Constant) else counts[iter.args[1].id].value

    assert(isinstance(start, int) and isinstance(end, int))

    # HACK(ss): checking if already declared the loop param
    declared_already = False
    for statement in operation_func.body:
        if isinstance(statement, AnnAssign) and statement.target.id == loop.target.id:
            declared_already = True
    if not declared_already:
        operation_func.body.insert(0,
                        AnnAssign(
                            target=Name(loop.target.id),
                            annotation=Name('int'),
                            simple=1
                        )
        )

    unrolled = []
    for i in range(start, end):
        unrolled.append(
            Assign(
                targets=[Name(loop.target.id)],
                value=Constant(i),
            )
        )
        unrolled.extend(loop.body)

    # Replace for loop in parent with unrolled statements
    parent.body[parent_body_idx:parent_body_idx+1] = unrolled

    do_unroll(module, loop_name)


def do_interchange(module: Module, loop_a_name: str, loop_b_name: str):
    operation_func: FunctionDef = None
    for node in module.body:
        if isinstance(node, FunctionDef):
            operation_func = node
            print(operation_func)
            
    assert(operation_func != None)

    # Find loops
    search = None
    loop_a = None
    loop_b = None
    for node in operation_func.body:
        print(node)
        if isinstance(node, For):
            if node.target.id == loop_a_name:
                print("loop_a_name")
                print(node.target.id)
                loop_a = node
            elif node.target.id == loop_b_name:
                print("loop_b_name")
                print(node.target.id)
                loop_b = node
            search = node
            break
    assert(search != None)

    while loop_a == None or loop_b == None:
        for node in search.body:
            if isinstance(node, For):
                if node.target.id == loop_a_name:
                    loop_a = node
                elif node.target.id == loop_b_name:
                    loop_b = node
                search = node

    # Swap, loop params
    loop_a_target_copy = copy.deepcopy(loop_a.target)
    loop_a_iter_copy   = copy.deepcopy(loop_a.iter)

    loop_a.target = loop_b.target
    loop_a.iter   = loop_b.iter

    loop_b.target = loop_a_target_copy
    loop_b.iter   = loop_a_iter_copy

def do_split(module: Module, to_split: str, outer: str, inner: str, factor: str):
    operation_func: FunctionDef = None
    for node in module.body:
        if isinstance(node, FunctionDef):
            operation_func = node
            break
    assert(operation_func != None)

    # Add declarations to start of function
    operation_func.body.insert(0,
                               AnnAssign(
                               target=Name(outer),
                               annotation=Name("int"),
                               simple=1
                               ))
    operation_func.body.insert(0,
                               AnnAssign(
                               target=Name(inner),
                               annotation=Name("int"),
                               simple=1
                               ))

    # Find first loop
    loop: For = None
    for node in operation_func.body:
        if isinstance(node, For):
            loop = node
            break
    assert(loop != None)

    # Find the loop to split
    while loop.target.id != to_split:
        for node in loop.body:
            if isinstance(node, For):
                loop = node

    body = copy.deepcopy(loop.body)

    new_inner = For(
        target=Name(inner),
        iter=Call(
            func=Name('n/a'),
            args=[Constant(0), Constant(int(factor)), Constant(1)]
        ),
        body=body,
    )

    loop_bounds = {
        "i0" : "m0",
        "j0" : "n0",
        "r0" : "(R)",
        "q0" : "(Q)",
    }

    # Replace split with outer, and have it's body be the new inner
    loop.target = Name(outer)
    loop.iter=Call(
                func=Name('n/a'), # Only have this because the Call class requires a func
                args=[Constant(0), Name(loop_bounds[to_split]), Constant(int(factor))]
    )
    loop.body=[new_inner]

    # Need to replace old index by the inner + outer
    # Add it's calculation to the kernel
    traverse = operation_func
    found = False
    while not found:
        for node in traverse.body:
            if isinstance(node, Assign) and node.targets[0].id == 'y[i0*n0+j0]':
                found = True
                break
            if isinstance(node, For):
                traverse = node

    traverse.body.insert(0,
                Assign(
                    targets=[Name(to_split)],
                    value=BinOp(Name(outer), Add(), Name(inner)),
                ))

# Modifies in place
def schedule_on_AST(module: Module, schedule_file_name: str):
    schedules = []
    with open(schedule_file_name, 'r') as file:
        for line in file:
            line = line.strip()
            schedule = Schedule_Type.UNKOWN
            args: List[str] = []

            if line.startswith("unroll"):
                schedule = Schedule_Type.UNROLL
                args = [line.split(' ')[1]]
            if line.startswith("interchange"):
                schedule = Schedule_Type.INTERCHANGE
                tokens = line.split(' ')
                args = [tokens[1], tokens[2]]
            if line.startswith("split"):
                schedule = Schedule_Type.SPLIT
                tokens = line.split(' ')
                args = tokens[1:]

            op_with_args = schedule, args
            schedules.append(op_with_args)
            
    for tup in schedules:
        schedule = tup[0]
        args = tup[1]

        match(schedule):
            case Schedule_Type.UNKOWN:
                print("Unkown schedule type encountered")
            case Schedule_Type.UNROLL:
                print("Unroll")
                assert(len(args) == 1)
                do_unroll(module, args[0])
            case Schedule_Type.INTERCHANGE:
                print("Interchange")
                assert(len(args) == 2)
                do_interchange(module, args[0], args[1])
            case Schedule_Type.SPLIT:
                print("Split")
                assert(len(args) == 4)
                do_split(module, args[0], args[1], args[2], args[3])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Need 3 arguments: [output_file_name] [operation_file_name] [schedule_file_name]")

    output_file_name = sys.argv[1]
    operation_file_name = sys.argv[2]
    schedule_file_name = sys.argv[3]

    module = operation_to_AST(operation_file_name)
    schedule_on_AST(module, schedule_file_name)

    gen = Gen_Code()
    generated_code = gen.gencode(module)

    with open(output_file_name, "w") as out:
        # For now not generating these just using templates
        out.write(template_defines + "\n")

        # Write the generated function and variables
        out.write(generated_code)

