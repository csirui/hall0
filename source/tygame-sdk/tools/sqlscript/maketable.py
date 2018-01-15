# -*- coding=utf-8 -*-

sql_schema = '''
DROP SCHEMA IF EXISTS `%s`;
CREATE SCHEMA IF NOT EXISTS `%s` CHARACTER SET utf8;
'''

sql_table = '''
DROP TABLE IF EXISTS `%s`.`t%d`;
CREATE TABLE `%s`.`t%d` (
  `userid` BIGINT UNSIGNED NOT NULL,
  `readtime` DATETIME NOT NULL,
  `writetime` DATETIME NOT NULL,
  `data` LONGTEXT NOT NULL,
  PRIMARY KEY (`userid`),
  INDEX `IDX_TIMES` (`readtime` ASC, `writetime` ASC))
  ENGINE = MyISAM
  CHARACTER SET utf8;
'''

def make_swap_table(schema_name):
    print sql_schema % (schema_name, schema_name)
    for x in xrange(100) :
        print sql_table % (schema_name, x, schema_name, x)
    print ''
    print ''

if __name__ == '__main__' :
    import sys
    make_swap_table(sys.argv[1])
