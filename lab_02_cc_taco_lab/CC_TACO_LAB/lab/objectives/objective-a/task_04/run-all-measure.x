#! /bin/bash
#
# Top level script to run verification in this directory.
# Note that the "-C" flag specifies the directory of the make file.

TASK_DIR=$(pwd)
FILE_OP_C=${TASK_DIR}/OP.c
BASELINE_FILE=baseline.c

# Note: you can fill out the following manually if you want to limit what is tested.
FILES_UNDER_TEST=$(ls test*.c)


# Reflexive test
make -C ../../.. measure-all OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${BASELINE_FILE}


# benchmark all files of the form test*.c
for i in `ls test*.c`
do
    echo $i
    make -C ../../.. measure-all OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/${BASELINE_FILE} FILE_TST=${TASK_DIR}/${i}
done

# NOTE: For every variant in the task (or test) make sure to run it in here if it is relevant.
. ../../venv/bin/activate; ls *.c.csv | xargs ../../plotter.py combined.png

