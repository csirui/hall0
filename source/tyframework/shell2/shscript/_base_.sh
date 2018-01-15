#!/bin/bash

export SLOG_FILE=${PATH_LOG}/script.out

function printout()
{
	msg=`date '+%F %T'`
	msg="${msg} ${PROCKEY} ${1} ${2} ${3} ${4} ${5} ${6} ${7} ${8} ${9}"
	echo ${msg} >> ${SLOG_FILE}
	echo ${msg}
}

export PYTHONUNBUFFERED=1
export PYPY_GC_MAX=4GB
export ACTION_TIME_OUT=300

cd ${PYTHONPATH}
