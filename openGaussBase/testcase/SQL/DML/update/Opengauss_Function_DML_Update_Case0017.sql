-- @testpoint: 子查询中使用between and、not like、not null、in、EXISTS的组合
-- @modify at: 2020-11-17
--建表
drop table if exists all_datatype_tbl;
create table all_datatype_tbl(c_integer integer, c_varchar varchar(50));
--插入数据
insert into all_datatype_tbl values(1,'aaaaa');
insert into all_datatype_tbl values(2,'bbbbb');
insert into all_datatype_tbl values(3,'ccccccccc');
insert into all_datatype_tbl values(4,'ddddddddddddd');
insert into all_datatype_tbl values(5,'eeeeeeeeeee');
select * from all_datatype_tbl;
update all_datatype_tbl t1 set (c_integer,c_varchar) =
(select c_integer c1,c_varchar c2 from all_datatype_tbl t2 where t1.c_integer=t2.c_integer+1 and t1.c_integer between 1 and 1000 and t1.c_varchar not like 'z'
and t1.c_varchar is not null and t1.c_integer in(2,3,4) and EXISTS(select * from all_datatype_tbl where t1.c_integer=c_integer+1 and t2.c_varchar=c_varchar));
select * from all_datatype_tbl order by 1;
--删表
drop table all_datatype_tbl;




