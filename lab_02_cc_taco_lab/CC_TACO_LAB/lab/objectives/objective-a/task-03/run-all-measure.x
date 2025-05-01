#!/bin/bash

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c

BASELINE_FILE=baseline.c
OPERATION_FILE=transpose.operation

python3 transpose_gen.py ${BASELINE_FILE} ../../../operation/${OPERATION_FILE}
make -C ../../.. measure-all OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${BASELINE_FILE}

. ../../../venv/bin/activate; ls *.c.csv | xargs ../../../plotter.py combined.png

