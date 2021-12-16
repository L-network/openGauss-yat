-- @testpoint: 函数sum(expression),所有输入行的expression总和，入参为无效值时，合理报错

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height dec(5,2),
hobbies text,
tel bigint
);
insert into table_test values(1, '张三', 12, 156.23, 'sings', 12355551895),
(7, '李四', 15, 146.45, 'read books', 12866661265),
(3, '李华', 18, 160.55, 'Dancing', 11822220366),
(5, '赵六', 18, 170.55, 'Playing games', 13344443322);

--当入参为非数值类型时
select sum(name) from table_test;
select sum(hobbies) from table_test;
drop table table_test;