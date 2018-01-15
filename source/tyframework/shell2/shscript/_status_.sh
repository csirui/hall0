#!/bin/bash
SHELL_FOLDER=$(cd `dirname ${0}`; pwd)

python ${SHELL_FOLDER}/python/status.py "$@"  2>&1
exit $?
