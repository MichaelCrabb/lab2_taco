#include <stdio.h>
#include <stdlib.h>

#include "instruments.h"

#include "COMPUTE.h"

#ifndef COMPUTE_NAME
#define COMPUTE_NAME pipelined
#endif

#ifndef COMPUTE_MODEL_NAME
#define COMPUTE_MODEL_NAME pipelined_model
#endif

void COMPUTE_MODEL_NAME( op_model_t   *model,
                         op_params_t  *op_params,
                         op_inputs_t  *inputs,
                         op_outputs_t *outputs,
                         op_inouts_t  *inouts,
                         hwctx_t      *hwctx )
{
  model->flops = op_params->m0;
  model->bytes = ((op_params->m0) + 1) * sizeof(float);
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
  float *z = inouts->z_scalar;

  /* local accumulators */
  float sum0 = 0.0f;
  float sum1 = 0.0f;
  float sum2 = 0.0f;
  float sum3 = 0.0f;

  BEGIN_INSTRUMENTATION;

  int i0 = 0;
  int limit = m0 / 4 * 4;  // largest multiple of 4 less than or equal to m0

  /* pipelined main loop */
  for (; i0 < limit; i0 += 4)
  {
    sum0 += x[i0];
    sum1 += x[i0 + 1];
    sum2 += x[i0 + 2];
    sum3 += x[i0 + 3];
  }

  /* handle leftover elements */
  for (; i0 < m0; ++i0)
  {
    sum0 += x[i0];
  }

  /* final accumulation */
  z[0] += (sum0 + sum1 + sum2 + sum3);

  END_INSTRUMENTATION;
}
