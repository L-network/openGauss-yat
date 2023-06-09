-- @testpoint: 修改表数据，同一字段，执行多次alter操作
-- @modify at: 2020-11-23
--建表
drop table if exists temp_table_alter_020;
create global temporary table temp_table_alter_020(
c_id int,
c_real real,
c_char char(50) default null,
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date
)on commit preserve rows;
--创建索引
drop index if exists temp_table_alter_020_idx1 cascade;
create index temp_table_alter_020_idx1 on temp_table_alter_020(c_id);
drop index if exists temp_table_alter_020_idx2 cascade;
create index temp_table_alter_020_idx2 on temp_table_alter_020(c_raw);
--插入数据
insert into temp_table_alter_020 values(1,1.0002,'dghg','jjjsdfghjhjui','010111100','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
insert into temp_table_alter_020 values(2,1.0002,'dghg','jjjsdfghjhjui','010111100','010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'));
insert into temp_table_alter_020 select * from temp_table_alter_020;
insert into temp_table_alter_020 select * from temp_table_alter_020;
insert into temp_table_alter_020 select * from temp_table_alter_020;
insert into temp_table_alter_020 select * from temp_table_alter_020;
insert into temp_table_alter_020 select * from temp_table_alter_020;
insert into temp_table_alter_020 select * from temp_table_alter_020;
--查询
select count(*) from temp_table_alter_020;
--删除索引
drop index temp_table_alter_020_idx2;
--修改列名
alter table temp_table_alter_020  rename column c_real to c_2;
--real类型改为varchar
alter table temp_table_alter_020 modify (c_2 varchar(20));
--修改数据类型执行多次
alter table temp_table_alter_020 modify (c_raw varchar(20));
alter table temp_table_alter_020 modify (c_raw raw(200));
--删表
drop table temp_table_alter_020 cascade;

