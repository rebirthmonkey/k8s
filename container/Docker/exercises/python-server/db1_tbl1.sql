# noinspection SqlNoDataSourceInspectionForFile
CREATE DATABASE db1;
USE db1;

CREATE TABLE IF NOT EXISTS `tbl1`(
   `tbl1_id` INT UNSIGNED AUTO_INCREMENT,
   `tbl1_title` VARCHAR(100) NOT NULL,
   `tbl1_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `tbl1_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO tbl1 (tbl1_title, tbl1_author, submission_date) VALUES
    ("aaa", "111", '2001-05-06'),
    ("bbb", "222", '2002-05-06'),
    ("ccc", "333", '2003-05-06'),
    ("ddd", "444", '2004-05-06'),
    ("eee", "555", '2005-05-06'),
    ("fff", "666", '2006-05-06'),
    ("ggg", "777", '2007-05-06'),
    ("hhh", "888", '2008-05-06'),
    ("iii", "999", '2009-05-06'),
    ("jjj", "000", '2010-05-06');
