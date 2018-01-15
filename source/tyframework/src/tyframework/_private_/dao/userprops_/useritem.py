# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst
from tyframework._private_.dao.userprops_.decorator.structdataitem import load_struct_data, \
    dump_struct_data


class UserItem(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_item_by_id(self, uid, gameid, itemid, item_cls):
        '''
        取得一个itemid对应内容, 将其内容实例化为item_cls类的新实例
        class类必须为使用 @struct_data_item 修饰的类
        返回: 依据item_cls的@struct_data_item的标记内容,返回@struct_data_item的实例或实例数组
        '''
        data = self.__ctx__.RedisGame.execute(uid, 'HGET', 'item:' + str(gameid) + ':' + str(uid), itemid)
        return load_struct_data(item_cls, data)

    def get_item_by_id_list(self, uid, gameid, itemid_list, item_cls):
        '''
        取得一个itemid_list集合中所有itemid对应的内容, 将所有内容实例化为item_cls类的新实例
        class类必须为使用 @struct_data_item 修饰的类
        返回: 数组, 每一项对应的item_cls的实例或数组
        '''
        datas = self.__ctx__.RedisGame.execute(uid, 'HMGET', 'item:' + str(gameid) + ':' + str(uid), *itemid_list)
        values = []
        for data in datas:
            obj = load_struct_data(item_cls, data)
            values.append(obj)
        return values

    def get_item_by_id_dict(self, uid, gameid, itemid_cls_dict):
        '''
        itemid_cls_dict为一个集合,
        key为itemid
        value为itmeid所对应的class类
        class类必须为使用 @struct_data_item 修饰的类
        返回: dict集合, key为itemid, value为对应的类的实例
        '''
        itemids = itemid_cls_dict.keys()
        datas = self.__ctx__.RedisGame.execute(uid, 'HMGET', 'item:' + str(gameid) + ':' + str(uid), *itemids)
        values = {}
        for x in xrange(len(itemids)):
            data = datas[x]
            itemid = itemids[x]
            item_cls = itemid_cls_dict[itemid]
            obj = load_struct_data(item_cls, data)
            values[itemid] = obj
        return values

    def update_item_by_id(self, uid, gameid, itemid, item_obj):
        '''
        更新一个item的内容, item_obj必须为使用@struct_data_item修饰过的类实例
        '''
        data = dump_struct_data(item_obj)
        self.__ctx__.RedisGame.execute(uid, 'HSET', 'item:' + str(gameid) + ':' + str(uid), itemid, data)

    def update_item_by_id_list(self, uid, gameid, itemid_list, item_value_list):
        '''
        更新一组item的内容, 
        itemid_list 为itemid的列表集合 
        item_value_list为itemid对应的数据集合
        item_value_list中的每一项,可以为单对象数据也可以为同一类的实例的list集合
        数据项目必须为使用@struct_data_item修饰过的类实例
        '''
        datas = []
        for x in xrange(len(itemid_list)):
            datas.append(itemid_list[x])
            datas.append(item_value_list[x])
        self.__ctx__.RedisGame.execute(uid, 'HMSET', 'item:' + str(gameid) + ':' + str(uid), *datas)

    def update_item_by_id_dict(self, uid, gameid, itemid_ins_dict):
        '''
        更新一组item的内容, itemid_ins_dict为一个dict, 
        key为itemid,value为itemid对应的数据值
        value可以为单对象数据也可以为同一类的实例的list集合
        数据项目必须为使用@struct_data_item修饰过的类实例
        '''
        datas = []
        for k, v in itemid_ins_dict.items():
            datas.append(k)
            datas.append(dump_struct_data(v))
        self.__ctx__.RedisGame.execute(uid, 'HMSET', 'item:' + str(gameid) + ':' + str(uid), *datas)

    def remove_item_by_id(self, uid, gameid, itemid):
        '''
        删除一个item
        '''
        self.__ctx__.RedisGame.execute(uid, 'HDEL', 'item:' + str(gameid) + ':' + str(uid), itemid)

    def remove_item_by_id_list(self, uid, gameid, itemid_list):
        '''
        删除一组item
        '''
        self.__ctx__.RedisGame.execute(uid, 'HDEL', 'item:' + str(gameid) + ':' + str(uid), *itemid_list)

    def insure_item_ids(self, uid, gameid, all_itemid_list):
        '''
        删除所有不再all_itemid_list中的其他的所有ID项目, 通常为整理数据内容时使用
        '''
        allids = set()
        for x in all_itemid_list:
            allids.add(str(x))
        delids = []
        rids = self.__ctx__.RedisGame.execute(uid, 'HKEYS', 'item:' + str(gameid) + ':' + str(uid))
        for rid in rids:
            if rid not in allids:
                delids.append(rid)
        if delids:
            self.__ctx__.RedisGame.execute(uid, 'HDEL', 'item:' + str(gameid) + ':' + str(uid), *delids)
