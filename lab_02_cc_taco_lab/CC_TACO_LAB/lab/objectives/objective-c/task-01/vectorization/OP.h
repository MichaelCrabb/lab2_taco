#ifndef _OP_H_
#define _OP_H_

#include "COMPUTE.h"

#define NUM_TRIALS         10
#define NUM_RUNS_PER_TRIAL 100

#if 1 // NOTE: USE 1 for real experiments, 0 for quick tests.
#define EXP_MIN_SIZE  16
#define EXP_MAX_SIZE  1524
#define EXP_STEP_SIZE 16
#else
#define EXP_MIN_SIZE  16
#define EXP_MAX_SIZE  256
#define EXP_STEP_SIZE 16
#endif

void op_params_finalize(op_params_t *op_params );
void op_inputs_finalize(op_inputs_t *op_inputs);
void op_outputs_finalize(op_outputs_t *op_outputs);
void op_inouts_finalize(op_inouts_t *op_inouts);

void benchmark_results_finalize(benchmark_results_t *bench_results);
void bench_config_finalize(benchmark_configuration_t *bench_config);

void op_params_init( int p, benchmark_configuration_t *bench_config, op_params_t *op_params );
void op_inputs_init(op_params_t *op_params, op_inputs_t *op_inputs);
void op_outputs_init(op_params_t *op_params, op_outputs_t *op_outputs);
void op_inouts_init(op_params_t *op_params, op_inouts_t *op_inouts);

void init_benchmark_results(benchmark_configuration_t *bench_config, benchmark_results_t *bench_results);

void op_inputs_copy_deep(op_inputs_t *op_inputs_src, op_inputs_t *op_inputs_dst);
void op_outputs_copy_deep(op_outputs_t *op_outputs_src, op_outputs_t *op_outputs_dst);
void op_inouts_copy_deep(op_inouts_t *op_inouts_src, op_inouts_t *op_inouts_dst);

void compute_benchmark_results( benchmark_configuration_t *bench_config,
				benchmark_results_t *bench_results,
				model_function_t *fun_compute_model,
				op_params_t  *op_params,
				op_inputs_t  *op_inputs_tst,
				op_outputs_t *op_outputs_tst,
				op_inouts_t  *op_inouts_tst,
				hwctx_t      *hw_ctx );

void compute_verifier_results(benchmark_configuration_t *bench_config,
			      op_params_t  *op_params,
			      op_outputs_t *op_outputs_tst,
			      op_outputs_t *op_outputs_ref,
			      op_inouts_t  *op_inouts_tst,
			      op_inouts_t  *op_inouts_ref);

void bench_config_init( int argc, char *argv[], benchmark_configuration_t *bench_config);
void bench_config_start_verifier(benchmark_configuration_t *bench_config);
void bench_config_start_timer(benchmark_configuration_t *bench_config);

#endif /* _OP_H_ */
