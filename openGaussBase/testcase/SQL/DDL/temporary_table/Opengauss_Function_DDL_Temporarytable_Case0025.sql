-- @testpoint: drop temporary语句，删除全局临时表，合理报错
--建表
drop  table if exists temp_table_025;
create global temporary table temp_table_025(
  t1 int,
  t2 blob);
--插入数据
insert into temp_table_025 values (1,'0101010');
select count(*) from temp_table_025;
--删表，报错
drop global temporary  table temp_table_025;
--删表
drop table temp_table_025;
