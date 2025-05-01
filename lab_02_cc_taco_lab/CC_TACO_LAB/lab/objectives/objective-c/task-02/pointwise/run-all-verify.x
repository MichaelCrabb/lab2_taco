#! /bin/bash
#
# Top level script to run verification in this directory.
# Note that the "-C" flag specifies the directory of the make file.

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c

BASELINE_FILE=baseline.c

# Reflexive test
make -C ../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${BASELINE_FILE}


# verify all files of the form test*.c
for i in `ls test*.c`
do
    echo $i
    make -C ../.. measure-verifier OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${i}
done
