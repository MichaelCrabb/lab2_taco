#!/usr/bin/env python3
import sys
from pathlib import Path

C_TEMPLATE = r"""
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

  model->flops =
    // (multiply & add flop) *m*n*k
    1*
    op_params->m0*
    op_params->n0;

  model->bytes =
    // Read and Write of C
    (2*(op_params->m0*op_params->n0)
     )*sizeof(float);
}





void COMPUTE_NAME( op_params_t  *op_params,
		   op_inputs_t  *inputs,
		   op_outputs_t *outputs,
		   op_inouts_t  *inouts,
		   hwctx_t   *hwctx )

{
  // dimensions
  const int m0 = op_params->m0;
  const int n0 = op_params->n0;


  // strides
  const int rs_a = op_params->rs_a;
  const int cs_a = op_params->cs_a;
  const int rs_c = op_params->rs_c;
  const int cs_c = op_params->cs_c;
  
  // buffers
  float *A = inputs->A_mat;
  float *C = inouts->C_mat;

  
  BEGIN_INSTRUMENTATION;
  for( int i0 = 0; i0 < m0; ++i0 )
    {
      for( int j0 = 0; j0 < n0; ++j0 )
	{
	  C[(j0*rs_c) + (i0*cs_c)] =
	    A[(i0*rs_a) + (j0*cs_a)];
	}
    }
  END_INSTRUMENTATION;
  

}
"""

def main() -> None:
    if len(sys.argv) != 2:
        prog = Path(sys.argv[0]).name
        print(f"Usage: {prog} <output_c_file>")
        sys.exit(1)

    output_path = Path(sys.argv[1])
    try:
        output_path.write_text(C_TEMPLATE.lstrip())
        print(f"[modified_generator] Wrote baseline kernel to {output_path}")
    except OSError as exc:
        print(f"[modified_generator] ERROR: could not write to {output_path}: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()