#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "COMPUTE.h"
#include "OP.h"

#include "timer.h"
#include "utils.h"


void benchmark_results_finalize(benchmark_results_t *bench_results)
{
  free(bench_results->results);
}

void bench_config_finalize(benchmark_configuration_t *bench_config)
{
  fclose(bench_config->result_file);
}


// finalize
void op_params_finalize(op_params_t *op_params )
{

}

void op_inputs_finalize(op_inputs_t *op_inputs)
{
  free(op_inputs->x_vect);
  free(op_inputs->y_scalar);
}

void op_outputs_finalize(op_outputs_t *op_outputs)
{
}

void op_inouts_finalize(op_inouts_t *op_inouts)
{
  free(op_inouts->z_vect);
}


// init
void op_params_init( int p, benchmark_configuration_t *bench_config, op_params_t *op_params )
{
  op_params->m0 = scale_p_on_pos_ret_v_on_neg(p,bench_config->in_m0);
}

void op_inputs_init(op_params_t *op_params, op_inputs_t *op_inputs)
{

  // Copy over data specfic params
  op_inputs->m0   = op_params->m0;

  op_inputs->num_elem_x_vect = op_inputs->m0;
  op_inputs->num_elem_y_scalar = 1;

  // Initialize the buffer
  op_inputs->x_vect = (float *)malloc(sizeof(float)*op_inputs->num_elem_x_vect);
  op_inputs->y_scalar = (float *)malloc(sizeof(float)*op_inputs->num_elem_y_scalar);

  // Fill the buffer with data
  fill_buffer_with_random( op_inputs->num_elem_x_vect, op_inputs->x_vect);
  fill_buffer_with_random( op_inputs->num_elem_y_scalar, op_inputs->y_scalar);
}

void op_outputs_init(op_params_t *op_params, op_outputs_t *op_outputs)
{

}

void op_inouts_init(op_params_t *op_params, op_inouts_t *op_inouts)
{
  op_inouts->m0 = op_params->m0;
  op_inouts->num_elem_z_vect = op_params->m0;

  // Initialize the buffer
  op_inouts->z_vect = (float *)malloc(sizeof(float)*op_inouts->num_elem_z_vect);

  // Fill the buffer with data
  fill_buffer_with_random( op_inouts->num_elem_z_vect, op_inouts->z_vect);
}


void init_benchmark_results(benchmark_configuration_t *bench_config, benchmark_results_t *bench_results)
{
  bench_results->results = (long *)malloc(sizeof(long)*bench_config->num_trials);
  bench_results->num_trials = bench_config->num_trials;
}


// deep_copy
void op_inputs_copy_deep(op_inputs_t *op_inputs_src, op_inputs_t *op_inputs_dst)
{
  // Copy over values
  op_inputs_dst->m0   = op_inputs_src->m0;

  op_inputs_dst->num_elem_x_vect = op_inputs_src->num_elem_x_vect;
  op_inputs_dst->num_elem_y_scalar = op_inputs_src->num_elem_y_scalar;


  // Copy the buffers.
  memcpy(op_inputs_src->x_vect,
	 op_inputs_dst->x_vect,
	 op_inputs_src->num_elem_x_vect*sizeof(float));

  memcpy(op_inputs_src->y_scalar,
	 op_inputs_dst->y_scalar,
	 op_inputs_src->num_elem_y_scalar*sizeof(float));

}

void op_outputs_copy_deep(op_outputs_t *op_outputs_src, op_outputs_t *op_outputs_dst)
{
}

void op_inouts_copy_deep(op_inouts_t *op_inouts_src, op_inouts_t *op_inouts_dst)
{
  op_inouts_dst->m0   = op_inouts_src->m0;
  op_inouts_dst->num_elem_z_vect = op_inouts_src->num_elem_z_vect;

  memcpy(op_inouts_src->z_vect,
	 op_inouts_dst->z_vect,
	 op_inouts_src->num_elem_z_vect*sizeof(float));


}

// processing results

void compute_verifier_results(benchmark_configuration_t *bench_config,
			      op_params_t  *op_params,
			      op_outputs_t *op_outputs_tst,
			      op_outputs_t *op_outputs_ref,
			      op_inouts_t  *op_inouts_tst,
			      op_inouts_t  *op_inouts_ref)
{
  float *output_diffs = (float *)malloc(op_inouts_ref->num_elem_z_vect*sizeof(float));

  // This will compute the error in between the strides of the values.
  float res = compute_pair_wise_diff(op_inouts_ref->num_elem_z_vect,1,1,1,
				     op_inouts_ref->z_vect,
				     op_inouts_tst->z_vect,
				     output_diffs);
  long counts = count_num_errors(op_inouts_ref->num_elem_z_vect,1,1,1,
				 output_diffs);

  // TODO: ADJUST THIS
  fprintf(bench_config->result_file, "%i, %li, %f, ",
	  op_params->m0,
	  counts, res);

  // if our error is greater than some threshold
  if( res > bench_config->error_threshold )
    fprintf(bench_config->result_file, "FAIL\n");
  else
    fprintf(bench_config->result_file, "PASS\n");

  free(output_diffs);

}


void compute_benchmark_results( benchmark_configuration_t *bench_config,
				benchmark_results_t *bench_results,
				model_function_t *fun_compute_model,
				op_params_t  *op_params,
				op_inputs_t  *op_inputs_tst,
				op_outputs_t *op_outputs_tst,
				op_inouts_t  *op_inouts_tst,
				hwctx_t      *hw_ctx )
{
  long min_res = pick_min_in_list(bench_results->num_trials, bench_results->results);
  float nanoseconds = ((float)min_res)/(bench_config->num_runs_per_trial);

  op_model_t model;

  fun_compute_model( &model,
		     op_params,
		     op_inputs_tst,
		     op_outputs_tst,
		     op_inouts_tst,
		     hw_ctx );


  // This gives us throughput as GFLOP/s
  double flop   =  model.flops;

  double throughput   =  flop / nanoseconds;
  double bytes        =  model.bytes;

  double gbytes_per_s =  bytes/ nanoseconds;

  // NOTE:OPERATION_SPECIFIC
  // "size,m,flop,throughput,bytes,GB_per_s,nanoseconds\n");
  fprintf(bench_config->result_file,
	  "%i,"
	  "%i,"
	  "%2.3e,%2.3e,"
	  "%2.3e,%2.3e,"
	  "%2.3e\n",
	  op_params->m0,

	  op_params->m0,

	  flop, throughput,
	  bytes, gbytes_per_s,
	  nanoseconds);

}

void bench_config_init( int argc, char *argv[], benchmark_configuration_t *bench_config)
{
  bench_config->num_trials         = NUM_TRIALS;
  bench_config->num_runs_per_trial = NUM_RUNS_PER_TRIAL;
  bench_config->error_threshold    = ERROR_THRESHOLD;

  // Get command line arguments
  if(argc == 1 )
    {
      // NOTE:OPERATION_SPECIFIC Adjust to reasonable defaults
      bench_config->min_size  = EXP_MIN_SIZE;
      bench_config->max_size  = EXP_MAX_SIZE;
      bench_config->step_size = EXP_STEP_SIZE;

      // defaults
      bench_config->in_m0=1;

      // default to printing to stdout
      bench_config->result_file = stdout;
    }
  else if(argc == 4 + 1 || argc == 5 + 1 )
    {
      bench_config->min_size  = atoi(argv[1]);
      bench_config->max_size  = atoi(argv[2]);
      bench_config->step_size = atoi(argv[3]);

      bench_config->in_m0=atoi(argv[4]);

      // default to printing to stdout
      bench_config->result_file = stdout;

      // If we were given a file, use that.
      if(argc == 5 + 1)
	bench_config->result_file = fopen(argv[5],"w");

    }
  else
    {
      //        argv 0   1    2    3  4        5
      printf("usage: %s min max step m0 [filename]\n",
	     argv[0]);
      exit(1);
    }


}

void bench_config_start_verifier(benchmark_configuration_t *bench_config)
{
  
}

void bench_config_start_timer(benchmark_configuration_t *bench_config)
{
  // print the first line of the output
  fprintf(bench_config->result_file,
	  "size,m,flop,throughput,bytes,GB_per_s,nanoseconds\n");
  
}

