#! /bin/bash
#
# Top level script to run verification in this directory.
# Note that the "-C" flag specifies the directory of the make file.

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c

BASELINE_FILE=baseline.c

TEST_FILE=test000.c
OP_DIR=operation/matvec.operation
NONE_DIR=schedules/basic/none.schedule

# Run this line in the case that the measure script is not ran first!
# python gen/mat_vec_gen.py ${TEST_FILE} ../../../${OP_DIR} ../../../${NONE_DIR}

# Reflexive test
make -C ../../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${BASELINE_FILE}


# verify all files of the form test*.c
# for i in `ls gen/test*.c`
# do
#     echo $i
#     make -C ../../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${i}
# done

make -C ../../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${TEST_FILE}
