-- @testpoint: 目标表和源表都存在，只用全称不用别名进行merge into操作
--step1: 创建目标表，源表并插入数据 ;expect: 成功
drop table if exists t_mergeinto_11_01;
drop table if exists t_mergeinto_11_02;
create table t_mergeinto_11_01(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_11_01 values (1501, 'vivitar 35mm', 'electrncs');
insert into t_mergeinto_11_01 values (1502, 'olympus is50', 'electrncs');
insert into t_mergeinto_11_01 values (1600, 'play gym', 'toys');
insert into t_mergeinto_11_01 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_11_01 values (1666, 'harry potter', 'dvd');
create table t_mergeinto_11_02(product_id integer,product_name varchar2(60),
category varchar2(60));
insert into t_mergeinto_11_02 values (1502, 'olympus camera', 'electrncs');
insert into t_mergeinto_11_02 values (1601, 'lamaze', 'toys');
insert into t_mergeinto_11_02 values (1666, 'harry potter', 'toys');
insert into t_mergeinto_11_02 values (1700, 'wait interface', 'books');
--step2: 进行merge into 操作; expect: 成功
merge into t_mergeinto_11_01    using t_mergeinto_11_02
on (t_mergeinto_11_01.product_id = t_mergeinto_11_02.product_id)
when matched then
  update set t_mergeinto_11_01.product_name = t_mergeinto_11_02.product_name,
   t_mergeinto_11_01.category = t_mergeinto_11_02.category
   where t_mergeinto_11_01.product_name != 'play gym'
when not matched then
  insert values (t_mergeinto_11_02.product_id, t_mergeinto_11_02.product_name,
  t_mergeinto_11_02.category) where t_mergeinto_11_02.category = 'books';
--step3: 查询更新后的结果; expect: 成功
select * from t_mergeinto_11_01 order by product_id;
--step4: 清理环境删除表 ; expect: 成功
drop table t_mergeinto_11_01;
drop table t_mergeinto_11_02;