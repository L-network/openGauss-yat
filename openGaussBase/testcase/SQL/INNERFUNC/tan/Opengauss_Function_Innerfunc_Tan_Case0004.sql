-- @testpoint: 数字操作函数，正切函数，可转成数值型的表达式

drop table if exists tan_T1;
create table tan_T1(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint);
insert into tan_T1(f1,f2,f3,f4,f5) values(0,22,33,44,55);
select tan(1+2-3*5) from sys_dummy;
select tan(-9+(2+4)/8) from sys_dummy;
select tan(f1+f2)from tan_T1;
drop table if exists tan_T1;

