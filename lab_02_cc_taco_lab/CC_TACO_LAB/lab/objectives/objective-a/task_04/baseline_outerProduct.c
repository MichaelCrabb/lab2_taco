/*
  This is a simple implementation of an outer product operation.

  - richard.m.veras@ou.edu

*/


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


// Dimensions of the Filter
static const int R = 4;
static const int Q = 3;

/* Weights of the Filter.
 - We are going to linearize this 2d array in row major order.
 - The following code illustrates the layout of the data
   and the relationship between a 2D array and its linearized
   counterpart.

  int NUMROWS=2;
  int NUMROWS=3;
 
  Arr2D[NUMROWS][NUMCOLS]=
                       // j= 0  1  2
                           {{a, b, c}, //  <-- i = 0
                            {d, e, f}}; // <-- i = 1
  Arr1D[NUMROWS*NUMCOLS];

  for( i=0; i<NUMROWS; ++i)
    for( j=0; j<NUMCOLS; ++j)
      Arr1D[i*NUMCOLS+j] = Arr2D[i][j]

 
      //   Arr1D[NUMROWS*NUMCOLS] |--->
      //         j=0  1  2
      //          {a, b, d,  <-- i=0
      //	   e, f, g   <-- i=1

*/

//weights[(Q)][(R)]
//weights[(Q)*(R)]
static float weights[] =
  //r=0    1     2     3
  {-1.1, -1.1,  1.2, -2.1,  // q=0
   -1.1, -2.1, -1.2,  2.2,  // q=1
   -2.1,  0.1,  0.2,  1.2}; // q=2




/*
  1 read           for x vector   (m)
  1 read           for y vector   (n)
  1 read + 1 write for C matrix   (m*n)
*/

void COMPUTE_MODEL_NAME( op_model_t   *model,
			 op_params_t  *op_params,
			 op_inputs_t  *inputs,
			 op_outputs_t *outputs,
			 op_inouts_t  *inouts,
			 hwctx_t      *hwctx )
{
  int m0 = op_params->m0;
  int n0 = op_params->n0;

  model->flops = 2*m0*n0; // One multiply and one add per element
  model->bytes = (m0 + n0 + 2*m0*n0)*sizeof(float); // Read x, read y, read+write C
}





void COMPUTE_NAME( op_params_t  *op_params,
		   op_inputs_t  *inputs,
		   op_outputs_t *outputs,
		   op_inouts_t  *inouts,
		   hwctx_t   *hwctx )

{
  int m0 = op_params->m0;
  int n0 = op_params->n0;

  float *x = inputs->x_vect;
  float *y = inputs->y_vect;
  float *C = inouts->C_mat;

  
  BEGIN_INSTRUMENTATION;
  // Outer product: C = x * y^T
  for( int i0 = 0; i0 < m0; ++i0 )
    {
      for( int j0 = 0; j0 < n0; ++j0 )
	{
	  C[i0*n0 + j0] = x[i0] * y[j0];
	}
    }
  END_INSTRUMENTATION;
  

}
