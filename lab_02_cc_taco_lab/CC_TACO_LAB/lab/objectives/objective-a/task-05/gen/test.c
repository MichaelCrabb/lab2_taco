
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
const int rs_a = op_params->rs_a;
const int cs_a = op_params->cs_a;
float * A = inputs->A_mat;
float * x = inputs->x_vect;
float * y = inouts->y_vect;
int i0;
int j0;
for (i0 = 0; i0 < m0; i0 += 1)
{
for (j0 = 0; j0 < n0; j0 += 1)
{
y[i0] = (y[i0] + (A[((i0 * rs_a) + (j0 * cs_a))] * x[j0]));

}

}

}
