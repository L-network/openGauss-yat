--  @testpoint:openGauss关键字defaults(非保留)，同时作为表名和列名带引号，并进行dml操作,defaults列的值最终显示为1000

drop table if exists "defaults";
create table "defaults"(
	c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
	c_real real, c_double real,
	c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
	c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
	c_date date, c_datetime date, c_timestamp timestamp,
	"defaults" varchar(100) default 'defaults'
)
PARTITION BY RANGE (c_integer)
(
	partition P_20180121 values less than (0),
	partition P_20190122 values less than (50000),
	partition P_20200123 values less than (100000),
	partition P_max values less than (maxvalue)
);



insert into "defaults"(c_id,"defaults") values(1,'hello');
insert into "defaults"(c_id,"defaults") values(2,'china');
update "defaults" set "defaults"=1000 where "defaults"='hello';
delete from "defaults" where "defaults"='china';
select "defaults" from "defaults" where "defaults"!='hello' order by "defaults";

drop table "defaults";

