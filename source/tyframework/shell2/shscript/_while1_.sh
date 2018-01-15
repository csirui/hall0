#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
source ${SHELL_FOLDER}/_base_.sh

LOG_FILE=${PATH_LOG}/${PROCLOG}

printout 'Hook Script Start'

while  [ 1 ]
do
	printout 'Hook Creat Process'
	printout `pwd` ${PYTHONPATH} ${PROCCLASS}
	mt=`date '+%F %T'`
	echo "${mt} shell _while1_ creat process ${PROCCLASS} ${PROCKEY}" >> ${LOG_FILE}
	${TASKSET} ${PYPY} ${PROCCLASS} ${PROCKEY} >> ${SLOG_FILE} 2>&1

	printout 'Found Hook Process missing.'

	if [ "${HOOKPROCESS}" = "hook" ]
	then
		nohup python ${SHELL_FOLDER}/python/sendmail.py "pypro_monitor@tuyoogame.com" "服务进程CRASH" "${PROCKEY}" >> ${SLOG_FILE} 2>&1 &
	else
		exit 1
	fi
done
