-- @testpoint: 验证创建二级分区表一级和二级分区键指定同一列，合理报错

drop table if exists mysql_partition_tab;
create table mysql_partition_tab(c1 int,c2 int,c3 int,c4 text,c5 text,c6 text,c7 text)
partition by range(c1) subpartition by range(c1) 
(
  partition p1 values less than (20000)
  (
    subpartition p1_1 values less than (10000),
    subpartition p1_2 values less than (20000)
  ),
  partition p2 values less than (40000)
  (
    subpartition p2_1 values less than (30000),
    subpartition p2_2 values less than (40000)
  )
);
