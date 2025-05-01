#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>

#include "instruments.h"

#include "COMPUTE.h"

#ifndef COMPUTE_NAME
#define COMPUTE_NAME vectorized
#endif

#ifndef COMPUTE_MODEL_NAME
#define COMPUTE_MODEL_NAME vectorized_model
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

  BEGIN_INSTRUMENTATION;

  __m128 vsum = _mm_setzero_ps();  // SSE 128-bit register initialized to 0

  int i0 = 0;
  int limit = m0 / 4 * 4;  // process 4 floats at a time

  for (; i0 < limit; i0 += 4)
  {
    __m128 vx = _mm_loadu_ps(&x[i0]);  // load 4 floats
    vsum = _mm_add_ps(vsum, vx);       // accumulate
  }

  // Horizontal sum the 4 floats inside vsum
  float temp[4];
  _mm_storeu_ps(temp, vsum);
  float final_sum = temp[0] + temp[1] + temp[2] + temp[3];

  // Handle leftover elements
  for (; i0 < m0; ++i0)
  {
    final_sum += x[i0];
  }

  z[0] += final_sum;

  END_INSTRUMENTATION;
}
