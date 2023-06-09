-- @testpoint: explain plan语句结合merge语句和when match,not match中update语句使用,合理报错
-- @modify at: 2020-11-12
--建表
drop table if exists explain_t1;
drop table if exists explain_t2;
drop table if exists explain_t3;
create table explain_t1(a int, b int);
create table explain_t2(f1 int,f2 int);
create table explain_t3(f3 int,f4 int);
--使用explain plan语句,成功
explain plan for merge into explain_t1 using explain_t2 on (explain_t1.a = explain_t2.f1)
when matched then update set b = (select f1 from explain_t2) where explain_t2.f2 = (select f3 from explain_t3)
when not matched then insert (a, b) values (explain_t2.f1, explain_t2.f1) where explain_t2.f1 = (select f3 from explain_t3);
--清理PLAN_TABLE表信息
delete from PLAN_TABLE;
--删表
drop table explain_t1;
drop table explain_t2;
drop table explain_t3;