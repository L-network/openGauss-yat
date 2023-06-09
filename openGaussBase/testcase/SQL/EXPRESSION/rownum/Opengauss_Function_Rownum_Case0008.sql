-- @testpoint: 测试rownum与排序的作用关系

drop table if exists student;
create table student
(
    s_id int primary key,
    s_name varchar(10) not null
);
insert into student values (2017100001, 'aaa');
insert into student values (2017100002, 'bbb');
insert into student values (2017100003, 'ccc');
insert into student values (2017100004, 'ddd');
insert into student values (2017100005, 'eee');
insert into student values (2017100006, 'fff');
--测试点1：测试排序和rownum生效先后关系
select * from student where rownum <= 4 order by 1 desc;
select * from student where rownum != 5 order by 1 asc;
--测试点2：子查询中包含排序
select * from (select * from student order by 1 desc) where rownum <= 4;
select * from (select * from student order by 1 asc) where rownum != 5;
--测试点3：对rownum进行排序
select rownum, * from student where rownum < 5 order by 1 desc;
select rownum rowno, * from student where rownum != 4 order by rowno desc;
select * from (select rownum rowno, * from student) where rowno != 4 order by rowno desc;
drop table if exists student;
