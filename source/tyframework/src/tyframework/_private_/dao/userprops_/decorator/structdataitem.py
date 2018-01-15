# -*- coding=utf-8 -*-

import struct


def struct_data_item(sformat=None, attrs=[], islist=0, version=0, att_version='version'):
    assert (isinstance(version, int))
    assert (version >= 0)

    assert (isinstance(islist, int))
    assert (islist == 0 or islist == 1)

    assert (isinstance(sformat, (str, unicode)))
    assert (len(sformat) > 0)

    if version > 0:
        assert (isinstance(att_version, (str, unicode)))
        assert (len(att_version) > 0)
        compile('dummyobj.' + att_version + ' = 0', 'attnamecheck', 'exec')  # test the att_version is ok
    else:
        att_version = ''

    assert (isinstance(attrs, (list, tuple)))
    assert (len(attrs) > 0)
    datas = []
    for x in attrs:
        assert (isinstance(x, (str, unicode)))
        compile('dummyobj.' + x + ' = 0', 'attnamecheck', 'exec')  # test the attname is ok
        datas.append(0)

    datasize = struct.calcsize(sformat)  # test sformat is ok
    struct.pack(sformat, *datas)  # test if the sformat is match to attrs ? insure all fromat is number 

    _ty_struct_define_ = {'version': version,
                          'att_version': att_version,
                          'sformat': sformat,
                          'attrs': attrs[:],
                          'attrs_len': len(attrs),
                          'islist': islist,
                          'datasize': datasize,
                          'pack_version': struct.pack('B', version)
                          }

    def clazz_warrp(clazz):
        olds = getattr(clazz, '_ty_struct_define_', {})
        olds[version] = _ty_struct_define_
        islist = olds.values()[0]['islist']
        if len(olds) > 1:
            islist = olds.values()[0]['islist']
            for v in olds.keys():
                if v == 0:
                    raise Exception('Can not mix data of version and no version (version=0 means no version)')
                if islist != olds[v]['islist']:
                    raise Exception('Can not mix data of list and no nolist')
        setattr(clazz, '_ty_struct_define_', olds)
        setattr(clazz, '_ty_struct_define_islist_', islist)
        setattr(clazz, '_ty_struct_define_version_', max(olds.keys()))
        return clazz

    return clazz_warrp


def __instance_clazz_obj(sinfos, sdata, clazz, notnone):
    datasize = sinfos['datasize']
    sformat = sinfos['sformat']
    attrs = sinfos['attrs']
    attrs_len = sinfos['attrs_len']
    if sdata and len(sdata) == datasize:
        datas = struct.unpack(sformat, sdata)
        if len(datas) == attrs_len:
            obj = clazz()
            att_version = sinfos['att_version']
            if att_version:
                version = sinfos['version']
                setattr(obj, att_version, version)
            for x in xrange(attrs_len):
                setattr(obj, attrs[x], datas[x])
            return obj
    if notnone:
        return clazz()
    return None


def __instance_struct_data(sinfos, clazz, data):
    islist = sinfos['islist']
    if islist:
        objs = []
        if data:
            bindex = 0
            datasize = sinfos['datasize']
            block = data[bindex: bindex + datasize]
            while len(block) == datasize:
                obj = __instance_clazz_obj(sinfos, block, clazz, 0)
                if obj:
                    objs.append(obj)
                bindex = bindex + datasize
                block = data[bindex: bindex + datasize]
        return objs
    else:
        return __instance_clazz_obj(sinfos, data, clazz, 1)


def load_struct_data(clazz, data):
    islist = getattr(clazz, '_ty_struct_define_islist_')
    if data == None or len(data) == 0:
        if islist:
            return []
        else:
            return clazz()
    try:
        data = data.encode('utf-8')
    except:
        pass

    _ty_struct_define_ = getattr(clazz, '_ty_struct_define_')
    version = getattr(clazz, '_ty_struct_define_version_')
    if version == 0:
        sinfos = _ty_struct_define_[0]  # must be 0 !!!!
        return __instance_struct_data(sinfos, clazz, data)

    if len(data) <= 1:
        if islist:
            return []
        else:
            return clazz()

    verstr = data[0:1]
    data = data[1:]
    dataver = struct.unpack('B', verstr)[0]
    if dataver in _ty_struct_define_:
        sinfos = _ty_struct_define_[dataver]
        return __instance_struct_data(sinfos, clazz, data)

    if islist:
        return []
    else:
        return clazz()


def __dump_struct_data(clazz, obj, needheadver):
    _ty_struct_define_ = getattr(clazz, '_ty_struct_define_')
    version = getattr(clazz, '_ty_struct_define_version_')
    sinfos = _ty_struct_define_[version]

    sformat = sinfos['sformat']
    attrs = sinfos['attrs']
    attrs_len = sinfos['attrs_len']
    sdatas = ''
    if needheadver == 0 and version > 0:
        sdatas = sinfos['pack_version']

    datas = []
    for x in xrange(attrs_len):
        value = getattr(obj, attrs[x], 0)
        datas.append(value)
    sdatas = sdatas + struct.pack(sformat, *datas)
    return sdatas


def dump_struct_data(objs):
    if not objs:
        return ''
    if isinstance(objs, (list, tuple)):
        sdatas = ''
        clazz = objs[0].__class__
        x = 0
        for obj in objs:
            if obj:
                if clazz != obj.__class__:
                    raise Exception(
                        'struct data must be the same class instance !! first:' + str(clazz) + ' found:' + str(
                            obj.__class__))
                sdata = __dump_struct_data(clazz, obj, x)
                sdatas = sdatas + sdata
                x += 1
        return sdatas
    else:
        clazz = objs.__class__
        return __dump_struct_data(clazz, objs, 0)
