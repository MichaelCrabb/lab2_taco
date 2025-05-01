#!/bin/bash

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c

BASELINE_FILE=baseline.c
OPERATION_FILE=reduction.operation

python3 reduction_gen.py ${BASELINE_FILE} ../../../operation/${OPERATION_FILE}
make -C ../../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=examples/00_reduction/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${BASELINE_FILE}


