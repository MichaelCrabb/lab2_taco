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
  model->flops = op_params->m0;
  model->bytes = 3 * (op_params->m0) * sizeof(float);
}

void COMPUTE_NAME( op_params_t  *op_params,
                   op_inputs_t  *inputs,
                   op_outputs_t *outputs,
                   op_inouts_t  *inouts,
                   hwctx_t      *hwctx )
{
  /* dimensions */
  const int m0 = op_params->m0;

  /* buffers */
  float *x = inputs->x_vect;
  float *y = inputs->y_vect;
  float *z = inouts->z_vect;
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      int i0 = i0_o * FACTOR + i0_i;
      
      z[i0] = x[i0] * y[i0];
    }
  }
  END_INSTRUMENTATION;
}
