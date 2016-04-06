CREATE DATABASE  IF NOT EXISTS `development_db`
USE `development_db`;

DROP TABLE IF EXISTS `Terms`;
CREATE TABLE `Terms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `terms` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `TermsURL`;
CREATE TABLE `TermsURL` (
  `termID` int(11) DEFAULT NULL,
  `urlID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `URL`;
CREATE TABLE `URL` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `title` longtext,
  `body_text` longtext,
  `links` longtext,
  `flag` tinytext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
