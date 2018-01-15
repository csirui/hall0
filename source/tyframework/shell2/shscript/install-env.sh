#!/bin/bash

SHELL_FOLDER=$(cd `dirname ${0}`; pwd)

PACKPATH=${SHELL_FOLDER}/python/

cd ${PACKPATH}

yum install python-devel -y

python get-pip.py

pip install redis --upgrade

pip install paramiko --upgrade

