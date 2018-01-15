#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
source ${SHELL_FOLDER}/_base_.sh

python ${SHELL_FOLDER}/python/hotcmd.py "$@" 2>&1
exit $?
