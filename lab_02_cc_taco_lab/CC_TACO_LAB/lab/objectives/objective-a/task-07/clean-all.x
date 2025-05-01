#!/bin/bash

BASELINE_SCHEDULE="baseline"

OPERATIONS=(
    "reduction"
    "scale"
    "pointwise"
    "transpose"
    "outerproduct"
    "matvec"
    "matmul"
)

for operation in "${OPERATIONS[@]}"; do
    pushd gen/${operation} > /dev/null
    TASK_DIR=$(pwd)
    FILE_OP_C=${TASK_DIR}/OP.c

    make -C ../../.. clean

    for i in `ls *.c`
    do
        echo $i
        make -C ../../../../.. clean-results OP_INCLUDE_DIR=${TASK_DIR} FILE_OP_C=${FILE_OP_C} FILE_REF=${TASK_DIR}/baseline.c FILE_TST=${TASK_DIR}/${i}
    done

    rm baseline.c
    rm -f baseline.c.measure.out baseline.c.cachemisses.out
    find . -maxdepth 1 -type f -name "*complex*" -exec rm -v {} \;
    popd > /dev/null
done

