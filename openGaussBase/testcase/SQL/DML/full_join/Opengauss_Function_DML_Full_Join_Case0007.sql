-- @testpoint:right join/left join/inner join/full join/union join混合使用查询
-- @modify at: 2020-11-13
--建表
drop table if exists all_datatype_table;
create table all_datatype_table(id int not null,c_intger integer,c_char char(10))
PARTITION BY RANGE (c_intger)
(
partition P_max values less than (2050)
);
--插入数据
insert into all_datatype_table values(1,1000,1000);
insert into all_datatype_table values(2,2000,1000);
insert into all_datatype_table values(3,2001,null);
insert into all_datatype_table values(4,2002,'a');
--查询
select count(*) from all_datatype_table t1 right join all_datatype_table t2 on t1.id=t2.id
inner join all_datatype_table t3 on t1.id=t3.id
full join all_datatype_table t10 on t1.id=t10.id
full join all_datatype_table t14 on t1.id=t14.id
right join all_datatype_table t15 on t1.id=t15.id
right join all_datatype_table t16 on t1.id=t16.id
full join all_datatype_table t17 on t1.id=t17.id
right join all_datatype_table t18 on t1.id=t18.id
right join all_datatype_table t19 on t1.id=t19.id where t2.id<3
union
select count(*) from all_datatype_table t1 right join all_datatype_table t2 on t1.id=t2.id
inner join all_datatype_table t3 on t1.id=t3.id
full join all_datatype_table t10 on t1.id=t10.id
full join all_datatype_table t14 on t1.id=t14.id
right join all_datatype_table t15 on t1.id=t15.id
right join all_datatype_table t16 on t1.id=t16.id
full join all_datatype_table t17 on t1.id=t17.id
right join all_datatype_table t18 on t1.id=t18.id
right join all_datatype_table t19 on t1.id=t19.id where t2.id<3;
--删表
drop table if exists all_datatype_table;