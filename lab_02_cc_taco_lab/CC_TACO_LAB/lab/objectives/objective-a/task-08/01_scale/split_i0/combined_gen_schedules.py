#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import Dict
from typing import Optional

TEMPLATES: Dict[str, str] = {
    "reduction": r"""

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
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      int i0 = i0_o * FACTOR + i0_i;
      
      z[0] += x[i0];
    }
  }
  END_INSTRUMENTATION;
}
""",

    "scale": r"""

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
  model->bytes = (2 * (op_params->m0) + 1) * sizeof(float);
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
  float *y = inputs->y_scalar;
  float *z = inouts->z_vect;
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      int i0 = i0_o * FACTOR + i0_i;
      
      z[i0] += x[i0] * y[0];
    }
  }
  END_INSTRUMENTATION;
}
""",

    "pointwise": r"""

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
""",

    "transpose": r"""

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
  model->flops = 1 * op_params->m0 * op_params->n0;
  model->bytes = 2 * (op_params->m0 * op_params->n0) * sizeof(float);
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

  /* strides */
  const int rs_a = op_params->rs_a;
  const int cs_a = op_params->cs_a;
  const int rs_c = op_params->rs_c;
  const int cs_c = op_params->cs_c;

  /* buffers */
  float *A = inputs->A_mat;
  float *C = inouts->C_mat;
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      for (int j0 = 0; j0 < n0; ++j0) {
        int i0 = i0_o * FACTOR + i0_i;
        
        C[(j0 * rs_c) + (i0 * cs_c)] = A[(i0 * rs_a) + (j0 * cs_a)];
      }
    }
  }
  END_INSTRUMENTATION;
}
""",

    "outerproduct": r"""

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
  model->flops = 2 * op_params->m0 * op_params->n0;
  model->bytes = (2 * (op_params->m0 * op_params->n0) +
                  op_params->m0 + op_params->n0) * sizeof(float);
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

  /* strides */
  const int rs_c = op_params->rs_c;
  const int cs_c = op_params->cs_c;

  /* buffers */
  float *x = inputs->x_vect;
  float *y = inputs->y_vect;
  float *C = inouts->C_mat;
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      for (int j0 = 0; j0 < n0; ++j0) {
        int i0 = i0_o * FACTOR + i0_i;
        
        C[(i0 * rs_c) + (j0 * cs_c)] += x[i0] * y[j0];
      }
    }
  }
  END_INSTRUMENTATION;
}
""",

    "matvec": r"""

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
  model->flops = 2 * op_params->m0 * op_params->n0;
  model->bytes = (2 * op_params->m0 +
                  op_params->m0 * op_params->n0 +
                  op_params->n0) * sizeof(float);
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

  /* strides */
  const int rs_a = op_params->rs_a;
  const int cs_a = op_params->cs_a;

  /* buffers */
  float *A = inputs->A_mat;
  float *x = inputs->x_vect;
  float *y = inouts->y_vect;
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR;

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      for (int j0 = 0; j0 < n0; ++j0) {
        int i0 = i0_o * FACTOR + i0_i;
          
        y[i0] += A[(i0 * rs_a) + (j0 * cs_a)] * x[j0];
      }
    }
  }
  END_INSTRUMENTATION;
}
""",

    "matmul": r"""

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
  
  int FACTOR = 4;
  int i0_o_bound = m0 / FACTOR;
  int i0_i_bound = FACTOR

  BEGIN_INSTRUMENTATION;
  for (int i0_o = 0; i0_o < i0_o_bound; ++i0_o) {
    for (int i0_i = 0; i0_i < i0_i_bound; ++i0_i) {
      for (int j0 = 0; j0 < n0; ++j0) {
        for (int p0 = 0; p0 < k0; ++p0) {
            int i0 = i0_o * FACTOR + i0_i;
            
            C[(i0 * rs_c) + (j0 * cs_c)] += A[(i0 * rs_a) + (p0 * cs_a)] * B[(p0 * rs_b) + (p0 * cs_b)];
        }
      }
    }
  }
  END_INSTRUMENTATION;
}
""",
}

def read_operation_file(path: Path) -> str:
    """Return the keyword inside a .operation file (lower‑cased, stripped)."""
    try:
        return path.read_text(encoding="utf-8").strip().lower()
    except OSError as exc:
        sys.exit(f"[generator] ERROR: cannot read '{path}': {exc}")

def infer_op_from_filename(fname: str, valid_ops: list[str]) -> Optional[str]:
    """Guess the operation keyword from the output filename stem."""
    stem = Path(fname).stem.lower()
    for op in valid_ops:
        if op in stem:
            return op
    return None

def usage(prog: str, valid_ops: list[str]) -> None:
    print(
        f"Usage:\n"
        f"  {prog} <output.c>                # infer op from filename\n"
        f"  {prog} <output.c> <opfile>       # opfile contains keyword\n"
        f"Valid ops: {', '.join(valid_ops)}"
    )
    sys.exit(1)

def main() -> None:
    argv = sys.argv
    prog = Path(argv[0]).name
    if len(argv) not in (2, 3):
        usage(prog, list(TEMPLATES))

    out_path = Path(argv[1])
    if len(argv) == 3:
        op_keyword = read_operation_file(Path(argv[2]))
    else:
        op_keyword = infer_op_from_filename(out_path.name, list(TEMPLATES))
        if op_keyword is None:
            usage(prog, list(TEMPLATES))

    template = TEMPLATES.get(op_keyword.lower())
    if template is None:
        usage(prog, list(TEMPLATES))

    try:
        out_path.write_text(template.lstrip())
        print(f"[generator] wrote {op_keyword} kernel to '{out_path}'")
    except OSError as exc:
        sys.exit(f"[generator] ERROR: cannot write '{out_path}': {exc}")

if __name__ == "__main__":
    main()