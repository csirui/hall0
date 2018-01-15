#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
source ${SHELL_FOLDER}/_base_.sh

printout "Start"

if [ "${REMOTE}" != "allnohup" ] 
then
	sh ${SHELL_FOLDER}/_stop_.sh >> ${SLOG_FILE} 2>&1
	if [ $? -ne 0 ]
	then
		printout "ERROR !! KILL Old Process !!"
	    exit 1
	fi
fi

export SHELL_START_TIME=`date +%s`

nohup ${SHELL_FOLDER}/_while1_.sh ${PROCKEY} >> ${SLOG_FILE} 2>&1 &
if [ $? -ne 0 ]
then
	printout " ERROR !!"
    exit 1
fi

python ${SHELL_FOLDER}/python/check_start.py >> ${SLOG_FILE} 2>&1
if [ $? -ne 0 ]
then
	printout " ERROR !!"
    # sh ${SHELL_FOLDER}/_stop_.sh >> ${SLOG_FILE} 2>&1
    exit 1
else
    printout " OK"
    exit 0
fi
