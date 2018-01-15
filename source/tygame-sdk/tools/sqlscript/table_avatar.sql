DROP SCHEMA IF EXISTS `beauty`;
CREATE SCHEMA IF NOT EXISTS `beauty` CHARACTER SET utf8;

DROP TABLE IF EXISTS `beauty`.`beauty_certify`;
CREATE TABLE `beauty`.`beauty_certify` (
  `user_id` bigint(20) unsigned NOT NULL,
  `game_id` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `timestamp` bigint(20) NOT NULL,
  `reason` char(64) not NULL,
  PRIMARY KEY (`user_id`),
  KEY `IDX_TS` (`timestamp`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
