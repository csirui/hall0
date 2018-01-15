# -*- coding=utf-8 -*-

from tyframework.decorator.structdataitem import struct_data_item


if __name__ == '__main__' :
    
    from tyframework._private_.dao.userprops_.decorator.structdataitem import dump_struct_data, load_struct_data
    
    print '测试1 : 适用于不需要改变的单项数据结构'
    @struct_data_item(sformat='3iB', attrs=['int1', 'int2', 'int3', 'int4'])
    class Test1(object):
        def __init__(self):
            self.int1 = 1
            self.int2 = 2
            self.int3 = 3
            self.int4 = 4
    data = dump_struct_data(Test1())
    print '测试1 :single dump->', repr(data)    
    t2 = load_struct_data(Test1, data)
    print '测试1 :single load->', t2.int1, t2.int2, t2.int3, t2.int4

    print '测试2 : 适用于不需要改变的复数项目数据结构'
    @struct_data_item(islist=1, sformat='3iB', attrs=['int1', 'int2', 'int3', 'int4'])
    class Test2(object):
        intx = 0
        def __init__(self):
            Test2.intx += 1
            self.int1 = Test2.intx
            Test2.intx += 1
            self.int2 = Test2.intx
            Test2.intx += 1
            self.int3 = Test2.intx
            Test2.intx += 1
            self.int4 = Test2.intx
    data = dump_struct_data([Test2() , Test2() , Test2() ])
    print '测试2 :list dump->', repr(data)    
    t2s = load_struct_data(Test2, data)
    for t2 in t2s :
        print '测试2 :list load->', t2.int1, t2.int2, t2.int3, t2.int4

    print '测试3 : 适用于可能会改变的的单项数据结构'
    @struct_data_item(version=1, sformat='<3iB', attrs=['int1', 'int2', 'int3', 'int4'])
    @struct_data_item(version=2, sformat='<3iBi', attrs=['int1', 'int2', 'int3', 'int4', 'int5'])
    class Test3(object):
        intx = 0
        def __init__(self):
            Test3.intx += 1
            self.int1 = Test3.intx
            Test3.intx += 1
            self.int2 = Test3.intx
            Test3.intx += 1
            self.int3 = Test3.intx
            Test3.intx += 1
            self.int4 = Test3.intx
            Test3.intx += 1
            self.int5 = Test3.intx
    t2 = Test3()
    print '测试3 :version single data->', t2.int1, t2.int2, t2.int3, t2.int4, t2.int5
    data = dump_struct_data(t2)
    print '测试3 :version single dump->', repr(data)    
    t2 = load_struct_data(Test3, data)
    print '测试3 :version single load->', t2.int1, t2.int2, t2.int3, t2.int4, t2.int5
    data = '\x01\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04'
    t2 = load_struct_data(Test3, data)
    print '测试3 :version single load ver 1->', t2.int1, t2.int2, t2.int3, t2.int4, t2.int5

    print '测试4 : 适用于可能会改变的的复数数据结构'
    @struct_data_item(version=1, islist=1, sformat='<3iB', attrs=['int1', 'int2', 'int3', 'int4'])
    @struct_data_item(version=2, islist=1, sformat='<3iBi', attrs=['int1', 'int2', 'int3', 'int4', 'int5'])
    class Test4(object):
        intx = 0
        def __init__(self):
            Test4.intx += 1
            self.int1 = Test4.intx
            Test4.intx += 1
            self.int2 = Test4.intx
            Test4.intx += 1
            self.int3 = Test4.intx
            Test4.intx += 1
            self.int4 = Test4.intx
            Test4.intx += 1
            self.int5 = Test4.intx
    data = dump_struct_data([Test4(), Test4(), Test4()])
    print '测试4 : version list dump->', repr(data)    
    t2s = load_struct_data(Test4, data)
    for t2 in t2s :
        print '测试4 : version list load->', t2.int1, t2.int2, t2.int3, t2.int4, t2.int5, t2.version
    data = '\x01\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x06'
    t2s = load_struct_data(Test4, data)
    for t2 in t2s :
        print '测试4 : version list load ver 1->', t2.int1, t2.int2, t2.int3, t2.int4, t2.int5, t2.version

