# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst
from tyframework._private_.dao.userprops_.decorator.structdataitem import load_struct_data, \
    dump_struct_data


class UserMedal(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_medal_by_id(self, uid, gameid, medalid, medal_cls):
        '''
        取得一个medalid对应内容, 将其内容实例化为medal_cls类的新实例
        class类必须为使用 @struct_data_item 修饰的类
        返回: 依据medal_cls的@struct_data_item的标记内容,返回@struct_data_item的实例或实例数组
        '''
        data = self.__ctx__.RedisGame.execute(uid, 'HGET', 'medal:' + str(gameid) + ':' + str(uid), medalid)
        return load_struct_data(medal_cls, data)

    def get_medal_by_id_list(self, uid, gameid, medalid_list, medal_cls):
        '''
        取得一个medalid_list集合中所有medalid对应的内容, 将所有内容实例化为medal_cls类的新实例
        class类必须为使用 @struct_data_item 修饰的类
        返回: 数组, 每一项对应的medal_cls的实例或数组
        '''
        datas = self.__ctx__.RedisGame.execute(uid, 'HMGET', 'medal:' + str(gameid) + ':' + str(uid), *medalid_list)
        values = []
        for data in datas:
            obj = load_struct_data(medal_cls, data)
            values.append(obj)
        return values

    def get_medal_by_id_dict(self, uid, gameid, medalid_cls_dict):
        '''
        medalid_cls_dict为一个集合,
        key为medalid
        value为itmeid所对应的class类
        class类必须为使用 @struct_data_item 修饰的类
        返回: dict集合, key为medalid, value为对应的类的实例
        '''
        medalids = medalid_cls_dict.keys()
        datas = self.__ctx__.RedisGame.execute(uid, 'HMGET', 'medal:' + str(gameid) + ':' + str(uid), *medalids)
        values = {}
        for x in xrange(len(medalids)):
            data = datas[x]
            medalid = medalids[x]
            medal_cls = medalid_cls_dict[medalid]
            obj = load_struct_data(medal_cls, data)
            values[medalid] = obj
        return values

    def update_medal_by_id(self, uid, gameid, medalid, medal_obj):
        '''
        更新一个medal的内容, medal_obj必须为使用@struct_data_item修饰过的类实例
        '''
        data = dump_struct_data(medal_obj)
        self.__ctx__.RedisGame.execute(uid, 'HSET', 'medal:' + str(gameid) + ':' + str(uid), medalid, data)

    def update_medal_by_id_list(self, uid, gameid, medalid_list, medal_value_list):
        '''
        更新一组medal的内容, 
        medalid_list 为medalid的列表集合 
        medal_value_list为medalid对应的数据集合
        medal_value_list中的每一项,可以为单对象数据也可以为同一类的实例的list集合
        数据项目必须为使用@struct_data_item修饰过的类实例
        '''
        datas = []
        for x in xrange(len(medalid_list)):
            datas.append(medalid_list[x])
            datas.append(medal_value_list[x])
        self.__ctx__.RedisGame.execute(uid, 'HMSET', 'medal:' + str(gameid) + ':' + str(uid), *datas)

    def update_medal_by_id_dict(self, uid, gameid, medalid_ins_dict):
        '''
        更新一组medal的内容, medalid_ins_dict为一个dict, 
        key为medalid,value为medalid对应的数据值
        value可以为单对象数据也可以为同一类的实例的list集合
        数据项目必须为使用@struct_data_item修饰过的类实例
        '''
        datas = []
        for k, v in medalid_ins_dict.items():
            datas.append(k)
            datas.append(dump_struct_data(v))
        self.__ctx__.RedisGame.execute(uid, 'HMSET', 'medal:' + str(gameid) + ':' + str(uid), *datas)

    def remove_medal_by_id(self, uid, gameid, medalid):
        '''
        删除一个medal
        '''
        self.__ctx__.RedisGame.execute(uid, 'HDEL', 'medal:' + str(gameid) + ':' + str(uid), medalid)

    def remove_medal_by_id_list(self, uid, gameid, medalid_list):
        '''
        删除一组medal
        '''
        self.__ctx__.RedisGame.execute(uid, 'HDEL', 'medal:' + str(gameid) + ':' + str(uid), *medalid_list)

    def insure_medal_ids(self, uid, gameid, all_medalid_list):
        '''
        删除所有不再all_medalid_list中的其他的所有ID项目, 通常为整理数据内容时使用
        '''
        allids = set()
        for x in all_medalid_list:
            allids.add(str(x))
        delids = []
        rids = self.__ctx__.RedisGame.execute(uid, 'HKEYS', 'medal:' + str(gameid) + ':' + str(uid))
        for rid in rids:
            if rid not in allids:
                delids.append(rid)
        if delids:
            self.__ctx__.RedisGame.execute(uid, 'HDEL', 'medal:' + str(gameid) + ':' + str(uid), *delids)
