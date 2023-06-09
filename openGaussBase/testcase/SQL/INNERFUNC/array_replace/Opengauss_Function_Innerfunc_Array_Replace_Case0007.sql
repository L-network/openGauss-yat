-- @testpoint: 替换数组array中所有的anyelement元素时,对于大小写null，空字符串的测试

select array_replace(array[1,2,2,3,null],NULL,4);
select array_replace(array[1,2,2,3,null],'',5);
select array_replace(array[1,2,2,3,null],null,5);
select array_replace(array[1.223,2,3.145,NULL],null,4.5);
select array_replace(array[1.223,2,3.145,NULL],NULL,66.0);
select array_replace(array[1.223,2,3.145,NULL],'',83.0);
select array_replace(array[1.223,2,3.145,''],NULL,'83');
select array_replace(array[-1.223,'',-3.145], null,89.0);
select array_replace(array[-1.223,'',-3.145],'','17.2');
select array_replace(array[true,false,null], null,'t');
select array_replace(array[true,false,null], NULL,'no');
select array_replace(array[true,false,NULL], NULL,'yes');
select array_replace(array[true,false,NULL], null,'1');
select array_replace(array['abc','efg',null], null,'table');
select array_replace(array['abc','efg',null], NULL,'schema');
select array_replace(array['abc','efg',null], '','view');
select array_replace(array['abc','efg',NULL], NULL,'source');
select array_replace(array['abc','efg',NULL],null,'index');
select array_replace(array['abc','efg',NULL], '','type');
select array_replace(array['abc','efg',''], NULL,'role');
select array_replace(array['abc','efg',''], null,'user');
select array_replace(array['abc','efg',''], '','data');
select array_replace(array['abc','efg','null'], 'null','replace');
select array_replace(array['abc','efg','NULL'], 'NULL','replace');
select array_replace(array['abc','efg','null'], '','replace');
select array_replace(array['abc','efg','NULL'], '','replace');
select array_replace(array['abc','efg','null'], 'NULL','replace');
select array_replace(array['abc','efg','NULL'], 'null','replace');