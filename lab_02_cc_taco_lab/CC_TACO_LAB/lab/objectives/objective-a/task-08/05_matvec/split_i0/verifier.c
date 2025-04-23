#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

#include "OP.h"
#include "COMPUTE.h"



int main( int argc, char *argv[] )
{
  hwctx_t hw_ctx;

  // What we will output to
  //  FILE *result_file;

  benchmark_configuration_t bench_config;
  bench_config_init( argc, argv, &bench_config);

  bench_config_start_verifier(&bench_config);
  
  // step through all of the problem sizes of interest
  for( int p = bench_config.min_size;
       p < bench_config.max_size;
       p += bench_config.step_size )
    {
      op_params_t  op_params;
      op_inputs_t  op_inputs_ref;
      op_inputs_t  op_inputs_tst;
      op_outputs_t op_outputs_ref;
      op_outputs_t op_outputs_tst;
      op_inouts_t  op_inouts_ref;
      op_inouts_t  op_inouts_tst;

      // create a set of parameters for the current experiment.
      op_params_init(p,&bench_config, &op_params );
      
      // Initialize the data
      op_inputs_init(&op_params, &op_inputs_ref);
      op_outputs_init(&op_params, &op_outputs_ref);
      op_inouts_init(&op_params, &op_inouts_ref);

      op_inputs_init(&op_params, &op_inputs_tst);
      op_outputs_init(&op_params, &op_outputs_tst);
      op_inouts_init(&op_params, &op_inouts_tst);

      // copy ref data to tst
      op_inputs_copy_deep(&op_inputs_ref,&op_inputs_tst);
      op_outputs_copy_deep(&op_outputs_ref,&op_outputs_tst);
      op_inouts_copy_deep(&op_inouts_ref,&op_inouts_tst);

      
      /*
	Run the reference
      */
	    
      // Perform the computation
      COMPUTE_NAME_REF( &op_params,
			&op_inputs_ref,
			&op_outputs_ref,
			&op_inouts_ref,
			&hw_ctx );


      
      // run the test
      // Perform the computation
      COMPUTE_NAME_TST( &op_params,
			&op_inputs_tst,
			&op_outputs_tst,
			&op_inouts_tst,
			&hw_ctx );

      // compute errors
      compute_verifier_results(&bench_config,
			       &op_params,
			       &op_outputs_tst,
			       &op_outputs_ref,
			       &op_inouts_tst,
			       &op_inouts_ref);
      
      // Free the  buffers
      op_inputs_finalize(&op_inputs_ref);
      op_inputs_finalize(&op_inputs_tst);
      
      op_outputs_finalize(&op_outputs_ref);
      op_outputs_finalize(&op_outputs_tst);
      
      op_inouts_finalize(&op_inouts_tst);
      op_inouts_finalize(&op_inouts_ref);

    }

  // close the result file
  bench_config_finalize(&bench_config);


}
