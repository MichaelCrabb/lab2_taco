#ifndef _COMPUTE_H
#define _COMPUTE_H

/*
  NOTE:OPERATION_SPECIFIC
  Checklist for adding a new operation:
  0. Structures

  1. Methods (which structs do they depend on)


  HARDWARE_TARGET_SPECIFIC
  checklist for calling an external function (messing with the build)
  
  Checklist for adding new hardware:
 */


/*
  TODO: Should be in it's own header.
  
  Hardware context

  Could include:
  + Distributed memory node
  (Physical Topology, virtual topology via Comm Groups)
  + Shared memory node
  (hostname)
  (#threads, numa domains, kaffinity, low-level memory organization: ctrls, channels, ranks, banks, rows, cols)
  + Core node (Kernels x Memory Movement x Comm)
  (HW threads, Vector Units, #ports, registers)
  + Acclerator
  (maybe just it's own shared node on a dist memory system....)
  +
  
*/
typedef struct hwctx_ts {
  int total_available_threads;
} hwctx_t;



// operation specific parameters
typedef struct op_params_ts {
  int m0;
} op_params_t;

typedef struct op_inputs_ts {
  int m0;

  // number of elements in a buffer for the matrices
  size_t num_elem_x_vect;
  size_t num_elem_y_scalar;
  

  float *x_vect;

  float *y_scalar;
} op_inputs_t;

typedef struct op_outputs_ts {
} op_outputs_t;

typedef struct op_inouts_ts {
  int m0;

  size_t num_elem_z_vect;

  // MxN
  float *z_vect;
} op_inouts_t;

typedef struct op_model_ts {
  float flops;
  float bytes;
} op_model_t;


typedef struct benchmark_configuration_ts
{
  // Experimental parameters
  int num_trials;
  int num_runs_per_trial;
  double error_threshold;
  
  // What we will output to
  FILE *result_file;
  
  // General Problem parameters
  int min_size;
  int max_size;
  int step_size;

  // NOTE:OPERATION_SPECIFIC
  int in_m0;

} benchmark_configuration_t ;

typedef struct benchmark_results_ts
{
  int num_trials;
  long *results;
} benchmark_results_t;



typedef void (benched_function_t)( op_params_t*,
				    op_inputs_t*,
				    op_outputs_t*,
				    op_inouts_t*,
				    hwctx_t*);

typedef void (model_function_t)( op_model_t*,
				 op_params_t*,
				 op_inputs_t*,
				 op_outputs_t*,
				 op_inouts_t*,
				 hwctx_t*);



void COMPUTE_NAME_REF( op_params_t  *op_params,
		       op_inputs_t  *inputs,
		       op_outputs_t *outputs,
		       op_inouts_t  *inouts,
		       hwctx_t   *hwctx );

void COMPUTE_NAME_TST( op_params_t  *op_params,
		       op_inputs_t  *inputs,
		       op_outputs_t *outputs,
		       op_inouts_t  *inouts,
		       hwctx_t   *hwctx );


void COMPUTE_MODEL_NAME_TST( op_model_t   *model,
			     op_params_t  *op_params,
			     op_inputs_t  *inputs,
			     op_outputs_t *outputs,
			     op_inouts_t  *inouts,
			     hwctx_t   *hwctx );

void COMPUTE_MODEL_NAME_REF( op_model_t   *model,
			     op_params_t  *op_params,
			     op_inputs_t  *inputs,
			     op_outputs_t *outputs,
			     op_inouts_t  *inouts,
			     hwctx_t   *hwctx );

#endif /* _COMPUTE_H */
