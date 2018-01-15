DROP SCHEMA IF EXISTS `ads`;
CREATE SCHEMA IF NOT EXISTS `ads` CHARACTER SET utf8;

DROP TABLE IF EXISTS `ads`.`clicks`;
CREATE TABLE `ads`.`clicks` (
  `iosappid` bigint(16) unsigned NOT NULL COMMENT 'ios应用标识',
  `clktime` bigint(12) unsigned NOT NULL COMMENT '首次点击时间',
  `spname` char(16) NOT NULL COMMENT '广告服务提供商',
  `clkip` char(128) COMMENT '点击时IP地址',
  `mac` char(17) COMMENT '设备MAC地址',
  `idfa` char(36) COMMENT '设备IDFA标识',
  `imei` char(15) COMMENT '设备IMEI标识',
  `clicks` int(8) COMMENT '点击总次数',
  `userid` bigint(10) unsigned COMMENT 'userid',
  `crttime` bigint(12) unsigned COMMENT '帐号创建时间',
  `acttime` bigint(12) unsigned COMMENT '帐号激活时间（玩三局）',
  `actip` char(128) COMMENT '激活时IP地址',
  `note` varchar(1024) COMMENT '扩展字段',
  PRIMARY KEY (`iosappid`, `spname`, `mac`, `idfa`, `imei`),
  INDEX `IDX_TIMES` (`clktime` ASC, `crttime` ASC, `acttime` ASC)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

