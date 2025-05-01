
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

void COMPUTE_MODEL_NAME(op_model_t *model, op_params_t *op_params, op_inputs_t *op_inputs, op_outputs_t *op_outputs, op_inouts_t *op_inouts, hwctx_t *hwctx)
{
model->flops = ((2 * op_params->m0) * op_params->n0);
model->bytes = (((((2 * (op_params->m0 * op_params->n0)) + op_params->m0) + op_params->n0) * sizeof(float)) * 1);

}
void COMPUTE_NAME(op_params_t *op_params, op_inputs_t *inputs, op_outputs_t *outputs, op_inouts_t *inouts, hwctx_t *hwctx)
{
const int m0 = op_params->m0;
const int n0 = op_params->n0;
const int rs_c = op_params->rs_c;
const int cs_c = op_params->cs_c;
float * x = inputs->x_vect;
float * y = inputs->y_vect;
float * C = inouts->C_mat;
int i0;
int j0;
for (j0 = 0; j0 < n0; j0 += 1)
{
for (i0 = 0; i0 < m0; i0 += 1)
{
BEGIN_INSTRUMENTATION ;
C[((i0 * rs_c) + (j0 * cs_c))] = (C[((i0 * rs_c) + (j0 * cs_c))] + (x[i0] * y[j0]));
END_INSTRUMENTATION ;

}

}

}
