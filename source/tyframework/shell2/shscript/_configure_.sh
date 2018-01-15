#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
source ${SHELL_FOLDER}/_base_.sh

printout "Configure"

python ${SHELL_FOLDER}/python/configure.py >> ${SLOG_FILE} 2>&1
exit $?
