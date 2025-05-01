
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

void COMPUTE_MODEL_NAME (op_model_t* model, op_params_t* op_params, op_inputs_t* inputs, op_outputs_t* outputs, op_inouts_t* inouts, hwctx_t* hwctx) {
  model->flops = 2 * op_params->m0 + 1 * sizeof(float);
  model->bytes = op_params->m0;
}

void COMPUTE_NAME (op_params_t* op_params, op_inputs_t* inputs, op_outputs_t* outputs, op_inouts_t* inouts, hwctx_t* hwctx) {
  const int m0 = op_params->m0;
  float* x = inputs->x_vect;
  float* y = inputs->y_scalar;
  float* z = inouts->z_vect;
  BEGIN_INSTRUMENTATION;
  for (int i0 = 0; i0 < m0; i0 += 1) {
  z[i0] += x[i0] * y[0];
  }
  END_INSTRUMENTATION;
}
