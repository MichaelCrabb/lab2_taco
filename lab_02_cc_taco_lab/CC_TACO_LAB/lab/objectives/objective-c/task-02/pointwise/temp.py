def generate_pointwise_AST() -> Module:
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
        Expr(
            value=Call(
                func=Name('BEGIN_INSTRUMENTATION'),
                args=[],
                keywords=[]
            )
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
                            value=Name('z'),
                            slice=Name('i0'),
                            ctx=Load()
                            ),
                        Eq(),
                        BinOp(
                            Subscript(
                                value=Name('x'),
                                slice=Name('i0'),
                                ctx=Load()
                            ),
                            Mult(),
                            Subscript(
                                value=Name('y'),
                                slice=Name('i0'),
                                ctx=Load()
                            )
                        )
                    )
                )
            ]
        ),
        Expr(
            value=Call(
                func=Name('END_INSTRUMENTATION'),
                args=[],
                keywords=[]
            )
        )
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