#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "OP.h"
#include "COMPUTE.h"

#include "timer.h"
#include "utils.h"




void time_function_under_test( benched_function_t function_under_test,
			       benchmark_configuration_t *bench_config,
			       benchmark_results_t *bench_results,
			       op_params_t  *op_params,
			       op_inputs_t  *inputs,
			       op_outputs_t *outputs,
			       op_inouts_t  *inouts,
			       hwctx_t   *hwctx )
{
  // Initialize the start and stop variables.
  TIMER_INIT_COUNTERS(stop, start);

  // Click the timer a few times so the subsequent measurements are more accurate
  TIMER_WARMUP(stop,start);

  // flush the cache
  flush_cache();
  
  for(int trial = 0; trial < bench_config->num_trials; ++trial )
    {

      /*
	Time code.
      */
      // start timer
      TIMER_GET_CLOCK(start);

      ////////////////////////
      // Benchmark the code //
      ////////////////////////

      for(int runs = 0; runs < bench_config->num_runs_per_trial; ++runs )
	{
	  function_under_test( op_params,
			       inputs,
			       outputs,
			       inouts,
			       hwctx );
	}

      ////////////////////////
      // End Benchmark      //
      ////////////////////////

        
      // stop timer
      TIMER_GET_CLOCK(stop);

      // subtract the start time from the stop time
      TIMER_GET_DIFF(start,stop,bench_results->results[trial]);
    }
}



int main( int argc, char *argv[] )
{
  
  /* TODO: MOVE
     command line argv --> hw_ctx (plen, vlen, funits, registers)
   */
  hwctx_t hw_ctx;

  
  // Problem parameters
  benchmark_configuration_t bench_config;
  bench_config_init( argc, argv, &bench_config);
  
  bench_config_start_timer(&bench_config);

  // step through all of the problem sizes of interest
  for( int p = bench_config.min_size;
       p < bench_config.max_size;
       p += bench_config.step_size )
    {

      op_params_t  op_params;
      op_inputs_t  op_inputs_tst;
      op_outputs_t op_outputs_tst;
      op_inouts_t  op_inouts_tst;
      
      // create a set of parameters for the current experiment.
      op_params_init(p,&bench_config, &op_params );
      
      
      // Initialize the data
      op_inputs_init(&op_params, &op_inputs_tst);
      op_outputs_init(&op_params, &op_outputs_tst);
      op_inouts_init(&op_params, &op_inouts_tst);

      
      // Perform the computation
      benchmark_results_t bench_results;
      init_benchmark_results(&bench_config,&bench_results);
      

      time_function_under_test( COMPUTE_NAME_TST,
				&bench_config,
				&bench_results,
				&op_params,
				&op_inputs_tst,
				&op_outputs_tst,
				&op_inouts_tst,
				&hw_ctx );


      /////////////////////
      // Compute the results

      model_function_t *model_fun = COMPUTE_MODEL_NAME_TST;
      compute_benchmark_results(&bench_config, &bench_results,
				model_fun,
				&op_params,
				&op_inputs_tst,
				&op_outputs_tst,
				&op_inouts_tst,
				&hw_ctx);

      //TODO: Put these in their own functions
      ///////
      benchmark_results_finalize(&bench_results);

      ///////

      //////////////////
      // Free the  buffers
      op_inputs_finalize(&op_inputs_tst);
      op_outputs_finalize(&op_outputs_tst);
      op_inouts_finalize(&op_inouts_tst);

    }


  // close the result file
  //fclose(bench_config.result_file);
  bench_config_finalize(&bench_config);
}
