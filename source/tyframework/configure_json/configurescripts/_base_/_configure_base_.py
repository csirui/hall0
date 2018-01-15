# -*- coding=utf-8 -*-

import json
from _base_._configure_helper_ import ConfigureHelper
import os

class RedisDatas(object):
    
    def __init__(self):
        self._datas_ = {}

    def add(self, key, value):
        assert(isinstance(key, (str, unicode)))
        self._datas_[key] = ConfigureHelper.clone_data(value)

class ConfigureBase(object):
    
    # 标准的以clientid区分的需要测试审核的数据
    STYLE_CLIENTID_STANDARD = '终端配置'
    # 全局的唯一,需要测试审核的数据
    STYLE_GLOBAL_WORK_FLOW_DATA = '全局配置'
    # 全局的唯一,不需要测试审核的数据, 例如一些再编辑界面做参考或模板的数据
    STYLE_REFERENCE = '数据参考'
    # 全局的唯一,专为直接编辑,保存即上线的数据
    STYLE_GLOBAL_ONLINE = '在线配置'

    # 缺省的CLIENTID名称
    CLIENTID_DEFAULT = 'default'

    def __init__(self):
        pass

    def get_info(self):
        '''
        取得当前对应的配置文件的描述信息
        返回集合：{"name" : "插件入口管理"}
        '''
        return {"name" : "请输入模块名称"}

    def get_data_style(self):
        '''
        取得当前对应的配置文件数据的数据类型
        返回 参考:ConfigureBase.STYLE_XXXX
        '''
        return self.STYLE_CLIENTID_STANDARD

    def verify_editor_data(self, datas):
        '''
        校验当前的数据文件的有效性
        返回错误信息集合 ["clientid无效", "必须输入名字"], 如果没有问题,则返回空集合或None
        datas为输入输出参数, 即界面编辑的数据, 校验包括: 数据类型校验转换, 有效性, 数据格式
        '''
        raise NotImplementedError

    def get_full_path_json_file(self, svntag, clientid):
        return ConfigureHelper.get_json_data_file_path(self, svntag, clientid)

    def read_datas(self, svntag, clientid):
        '''
        读取编辑界面的数据
        目前,只有server_list需要覆盖此方法, 每次读取都重全局配置服务器进行读取
        '''
        jsonfile = ConfigureHelper.get_json_data_file_path(self, svntag, clientid)
        if not os.path.isfile(jsonfile) :
            ConfigureHelper.add_json_data_file(svntag, clientid, jsonfile)
            jsonfile = ConfigureHelper.get_json_data_file_path(self, svntag, 'default') # 方便界面显示 2015-04-07
            return ConfigureHelper.read_json_data_file(jsonfile)
            
        datas = ConfigureHelper.read_json_data_file(jsonfile)
        if datas :
            return datas
        
        jsonfile = ConfigureHelper.get_json_data_file_path(self, svntag, 'default') # 方便界面显示 2015-04-07
        return ConfigureHelper.read_json_data_file(jsonfile)
    
    def write_datas(self, svntag, clientid, datas):
        '''
        保存编辑界面的数据
        目前,只有server_list需要覆盖此方法, 以便在保存时同步通知全局配置服务器进行服务列表的更新操作
        '''
        jsonfile = ConfigureHelper.get_json_data_file_path(self, svntag, clientid)
        ConfigureHelper.write_json_data_file(jsonfile, datas)
        return jsonfile

    def generate_redis_datas(self, datas, redisdata):
        '''
        说明: 将界面编辑数据转换到REDIS数据格式, 
            例如: 剔除界面编辑中的一些修改备注信息等
                 或者转换列表到字典等操作
        参数: datas 界面编辑数据
             redisdata REDIS数据输出对象, RedisDatas的实例
        例如:
            当数据类型为 STYLE_GLOBAL_WORK_FLOW_DATA 时:
                redisdata.add('global.gameids', {"1" : "金花", "2" : "方块"})
                最终将产生REDIS命令: 
                SET 'configitems:global.gameids' '{"1":"金花","2":"方块"}'

            当数据类型为 STYLE_CLIENTID_STANDARD 时:
                redisdata.add('games:9999:uiswitches', [{"name" : "more_games","open" : 1}])
                假定共有2个clientid : Andorid_3.1_360, Andorid_3.2_kugou
                最终将产生REDIS命令: 
                SET 'configitems:games:9999:uiswitches:Andorid_3.1_360'   '[{"name" : "more_games","open" : 1}]'
                SET 'configitems:games:9999:uiswitches:Andorid_3.2_kugou' '[{"name" : "more_games","open" : 1}]'
        '''
        return None

    def generate_redis_datas_recursive(self, jsonfile, datas, redisdata, **kwargs):
        """
        将json中定义的数据转换成REDIS数据格式，支持目录递归
        :param jsonfile:
        :param datas:
        :param redisdata:
        :param kwargs:
        :return:
        """
        raise NotImplementedError("TO BE IMPLEMENTED")

    def data_int(self, datadict, key):
        try:
            return int(datadict.get(key, None))
        except:
            return None

    def data_float(self, datadict, key):
        try:
            return float(datadict.get(key, None))
        except:
            return None

    def data_str(self, datadict, key):
        try:
            return unicode(datadict.get(key, None))
        except:
            return None

    def clone_data(self, data):
        return json.loads(json.dumps(data))
