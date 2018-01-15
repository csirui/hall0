# -*- coding=utf-8 -*-

import os
from _base_._configure_helper_ import ConfigureHelper
from _base_._configure_base_ import ConfigureBase, RedisDatas

def make_all_configure_cmds(main_file):
    
    workpath = os.path.dirname(os.path.abspath(main_file))
    svnrootpath = os.path.dirname(workpath)
    svnrootpath = os.path.dirname(svnrootpath)
    svnrootpath = os.path.dirname(svnrootpath)+ '/tydatas'
    if not os.path.isdir(svnrootpath) :
        svnrootpath = os.path.dirname(workpath)

    print '装载配置PY文件目录: %s' % (workpath)
    print '装载配置DATA文件目录: %s' % (svnrootpath)

    ConfigureHelper.load_all_models(workpath, svnrootpath, None, None)

    sfile = os.environ.get('CONFIGURE_SERVICE_FILE')
    service = ConfigureHelper.read_json_data_file(sfile)
    service = ConfigureHelper.decode_utf8_objs(service)

    outputsfile = os.environ.get('CONFIGURE_OUTPUTS_FILE')
    outputs = ConfigureHelper.read_json_data_file(outputsfile)
    outputs = ConfigureHelper.decode_utf8_objs(outputs)
    if not 'configuredatas' in outputs :
        outputs['configuredatas'] = {}
    configuredatas = outputs['configuredatas']

    if not 'cmdkeys' in outputs :
        outputs['cmdkeys'] = {}
    cmdkeys = outputs['cmdkeys']

    if service['mode'] == 1 :
        if service['simulation'] == 1 :
            svn_tag = 'tag-simulation'
        else:
            svn_tag = 'tag-online'
    else:
        svn_tag = 'tag-edit'
    
    svn_tag = 'tag-edit' # TODO 目前没有走全部流程, 配置全在tag-edit下

    x = 0
    for key, minfo in ConfigureHelper.CACHE.items() :
        x += 1
        model = minfo['instance']
        dstyle = model.get_data_style()
        print '装载配置模块 [%d/%d] : %s/%s' % (x, len(ConfigureHelper.CACHE), workpath, key)

        if dstyle in (ConfigureBase.STYLE_REFERENCE, ConfigureBase.STYLE_GLOBAL_ONLINE) :
            print dstyle, key, '无需生成配置内容'
            continue

        fullpath = model.get_full_path_json_file(svn_tag, 'default')
        fullpath = os.path.dirname(fullpath)
        jsonfiles = ConfigureHelper.find_sub_files(fullpath, '.json')
        if not jsonfiles :
            print key, '没有找到JSON配置文件'

        for jsonfile in jsonfiles :
            jsonpath = fullpath + '/' + jsonfile
            print '装载数据文件:' , jsonpath
            datas = ConfigureHelper.read_json_data_file(jsonpath, True)
            datas = ConfigureHelper.decode_utf8_objs(datas)
            redisdata = RedisDatas()
            try:
                model.generate_redis_datas_recursive(jsonfile, datas, redisdata)
            except NotImplementedError:
                model.generate_redis_datas(datas, redisdata)
            
            clientid = None
            if dstyle == ConfigureBase.STYLE_CLIENTID_STANDARD :
                clientid = jsonpath.split('/')[-1][0:-5]

            for rkey, rvalue in redisdata._datas_.items() :
                rkey = 'configitems:' + rkey
                if clientid :
                    rkey = rkey + ':' + clientid
                if not rkey in cmdkeys :
                    cmdkeys[rkey] = 1
                    configuredatas[rkey] = rvalue
                else:
                    raise Exception('The configitems key already exits !! [' + rkey + ']')

    ConfigureHelper.write_json_data_file(outputsfile, outputs)
    print '装载配置文件目录: %s 完成' % (workpath)

if __name__ == '__main__' :
    make_all_configure_cmds()
    
