# -*- coding=utf-8 -*-

sql_table = '''
DELETE FROM `%s`.`t%d`;
'''

def make_swap_table(schema_name):
    print 'use', schema_name, ';'
    for x in xrange(100) :
        print sql_table % (schema_name, x)
    print ''
    print ''

if __name__ == '__main__' :
    import sys
    schemas = ['tyuser', 'tygame1', 'tygame2', 'tygame3', 'tygame4', 'tygame5', 'tygame6',
               'tygame7', 'tygame8', 'tygame9', 'tygame10', 'tygame11', 'tygame12', 'tygame9999', ]
    for s in schemas :
        make_swap_table(s)
