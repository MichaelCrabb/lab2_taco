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

void COMPUTE_MODEL_NAME( op_model_t   *model,
                         op_params_t  *op_params,
                         op_inputs_t  *inputs,
                         op_outputs_t *outputs,
                         op_inouts_t  *inouts,
                         hwctx_t      *hwctx )
{
  model->flops = 2 * op_params->m0 * op_params->n0 * op_params->k0;
  model->bytes = (2 * (op_params->m0 * op_params->n0) +
                  (op_params->m0 * op_params->k0) +
                  (op_params->k0 * op_params->n0)) * sizeof(float);
}

void COMPUTE_NAME( op_params_t  *op_params,
                   op_inputs_t  *inputs,
                   op_outputs_t *outputs,
                   op_inouts_t  *inouts,
                   hwctx_t      *hwctx )
{
  /* dimensions */
  const int m0 = op_params->m0;
  const int n0 = op_params->n0;
  const int k0 = op_params->k0;

  /* strides */
  const int rs_a = op_params->rs_a;
  const int cs_a = op_params->cs_a;
  const int rs_b = op_params->rs_b;
  const int cs_b = op_params->cs_b;
  const int rs_c = op_params->rs_c;
  const int cs_c = op_params->cs_c;

  /* buffers */
  float *A = inputs->A_mat;
  float *B = inputs->B_mat;
  float *C = inouts->C_mat;

  BEGIN_INSTRUMENTATION;
  for (int i0 = 0; i0 < m0; ++i0) {
    for (int j0 = 0; j0 < n0; ++j0) {
      for (int p0 = 0; p0 < k0; ++p0) {
        C[(i0 * rs_c) + (j0 * cs_c)] += A[(i0 * rs_a) + (p0 * cs_a)] * B[(p0 * rs_b) + (p0 * cs_b)];
      }
    }
  }
  END_INSTRUMENTATION;
}
