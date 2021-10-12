-- @testpoint: update语句中的子查询中使用EXISTS子句
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
--修改数据
update all_datatype_tbl t1 set (c_integer,c_varchar) = (select c_integer c1,c_varchar c2 from all_datatype_tbl t2 where t1.c_integer=t2.c_integer+1 and EXISTS(select * from all_datatype_tbl where t1.c_integer=c_integer+1 and t2.c_varchar=c_varchar));
select * from all_datatype_tbl order by 1;
--删表
drop table all_datatype_tbl;
