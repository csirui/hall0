# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, mylog
from _main_thread_ import exec_index_script_on_first_server, \
    get_status_json_datas

def execute_hot_cmd(actparams, act_name, hotcmd_params):
    
    mylog.log('开始' + act_name)
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    service = params['service']
    script = service['_script_hotcmd_']
    status, outputs = exec_index_script_on_first_server(params, script, hotcmd_params)
    if status != 0 :
        mylog.error(act_name + '失败')
        mylog.error(outputs)
        return 0
    
    datas = get_status_json_datas(outputs)
    
    if datas.get('result', -1) != 0 :
        mylog.log(act_name + '失败')
        mylog.error(outputs)
        return 0

    iserror = 0
    process = datas.get('process')
    if isinstance(process, dict) :
        for prockey, presult in process.items() :
            result = presult.get('result', {})
            ok = result.get('ok', 0)
            if ok != 1 :
                iserror = 1
                mylog.error(prockey, result, presult.get('error', {}))
            else:
                mylog.log(prockey, result)

    if iserror :
        mylog.log(act_name + '失败')
        return 0

    mylog.log(act_name + '成功')
    return 1
