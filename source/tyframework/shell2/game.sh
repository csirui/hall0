#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)

export PYTHONUNBUFFERED=1
pypy ${SHELL_FOLDER}/_pygamecontrol_/_main_.py "$@"
_RET_=$?
echo "=== game.sh done ==="
exit ${_RET_}
