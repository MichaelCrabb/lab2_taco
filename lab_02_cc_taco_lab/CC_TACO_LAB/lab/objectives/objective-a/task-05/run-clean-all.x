#! /bin/bash
#
# Top level script to run verification in this directory.
# Note that the "-C" flag specifies the directory of the make file.

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c

TEST_FILE=test000.c
OP_DIR=operation/matvec.operation
NONE_DIR=schedules/basic/none.schedule

# for i in `ls *.c`
# do
#     echo $i
#     make -C ../.. clean-results OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/baseline.c FILE_TST=${TASK_DIR}/${i}
# done

# Reflexive cleaning 
make -C ../../.. clean-results OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/baseline.c FILE_TST=${TASK_DIR}/baseline.c

# Test file cleaning
make -C ../../.. clean-results OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/baseline.c FILE_TST=${TASK_DIR}/${TEST_FILE}

rm ${TEST_FILE}
rm combined.png
