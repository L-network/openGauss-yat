--  @testpoint:
drop schema if exists tpcds;
create schema tpcds;
--创建表reason
CREATE TABLE tpcds.reason (
    CD_DEMO_SK          INTEGER          NOT NULL,
    CD_GENDER           character(16)            ,
    CD_MARITAL_STATUS   character(100)
);
--插入数据
INSERT INTO tpcds.reason VALUES(51, 'AAAAAAAADDAAAAAA', 'reason 51');
--创建表reason_t1
CREATE TABLE tpcds.reason_t1 AS TABLE tpcds.reason;
--为一个INSERT语句创建一个预备语句然后执行它
PREPARE insert_reason(integer,character(16),character(100)) AS INSERT INTO tpcds.reason_t1 VALUES($1,$2,$3);
EXECUTE insert_reason(52, 'AAAAAAAADDAAAAAA', 'reason 52');
--删除预备语句
deallocate insert_reason;
DROP TABLE tpcds.reason;
DROP TABLE tpcds.reason_t1;
drop schema tpcds;

