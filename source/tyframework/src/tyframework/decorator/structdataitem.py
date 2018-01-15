# -*- coding=utf-8 -*-

'''
struct pack/unpack 标记
说明:
    用于自动化的对数据pack和unpack, 并生成对应的类实例
    @struct_data_item(sformat=None, attrs=[], islist=0, version=0, att_version='version')
    sformat : struct使用的标准的数据格式, 例如"<3iB"
    attrs : 进行数据<->类实例转换过程中, 属性设定列表和数据的取得列表
    islist : 数据存取时, 是否按照列表的格式进行存储
            islist = 0 时, 3iB存储数据格式为: '\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04'
            islist = 1 时, 3iB存储数据格式为: '\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04' + '\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04' + ...
    version : 数据格式的版本号, 当 version > 0 时, 才在存储中保留版本号(一个字节, 0xFF, 最多255个版本)
              version主要用于数据结构变更时使用, 在再次保存时,数据结构将存储为最新的(最大的version)的数据格式
    att_version : 当 version > 0 时,生成类实例时version保存的类属性的名称
    详细用法, 请参考实际测试示例: tyframework-trunk/test/tytest/tyframework/structdataitem.py
'''

from tyframework._private_.dao.userprops_.decorator.structdataitem import struct_data_item

struct_data_item = struct_data_item
