SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
cd ${SHELL_FOLDER}
rm -fr ./action.log ./logs/* ./bireport/* ./backup/*
sh ./source/tyframework/shell2/game.sh -m ./source/tygame-sdk/configure/server/test_127001.json -noback -a start
