-- @testpoint: overlay函数与数值函数结合使用
SELECT overlay(abs('-221423.1') placing 'world' from 2 for 3 );
SELECT overlay(acos(-0.9)placing 'world'from 2 for 3);