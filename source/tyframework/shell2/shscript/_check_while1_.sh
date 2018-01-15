#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
source ${SHELL_FOLDER}/_base_.sh

printout "Check _while1_"

python ${SHELL_FOLDER}/python/check_while1.py >> ${SLOG_FILE} 2>&1
exit $?
