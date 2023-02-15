-- @testpoint: cast用例
set time zone 'uct';
-- 将转换的某个常量插入表中，查看结果应为转换后的值
-- 新建表
create table t_Opengauss_CAST_Case0030_1(a int,c money,b timestamp);
-- 插入数据
insert into t_Opengauss_CAST_Case0030_1 values(1,2,cast(cast('2022-11-10 18:03:20'::timestamp as unsigned) as timestamp));
insert into t_Opengauss_CAST_Case0030_1 values(2,cast(cast('$2'::money as unsigned) as money),cast(cast('2022-11-10 18:03:20'::timestamp as unsigned) as timestamp));
-- 查询数据
select * from t_Opengauss_CAST_Case0030_1;
-- 清理环境
drop table t_Opengauss_CAST_Case0030_1;
