--  @testpoint:opengauss关键字merge(非保留)，MERGE INTO 将目标表和源表中数据针对关联条件进行匹配
CREATE TABLE products
(
product_id INTEGER,
product_name VARCHAR2(60),
category VARCHAR2(60)
);

 INSERT INTO products VALUES (1501, 'vivitar 35mm', 'electrncs');
 INSERT INTO products VALUES (1502, 'olympus is50', 'electrncs');
 INSERT INTO products VALUES (1600, 'play gym', 'toys');
 INSERT INTO products VALUES (1601, 'lamaze', 'toys');
 INSERT INTO products VALUES (1666, 'harry potter', 'dvd');

CREATE TABLE newproducts
(
product_id INTEGER,
product_name VARCHAR2(60),
category VARCHAR2(60)
);
 INSERT INTO newproducts VALUES (1502, 'olympus camera', 'electrncs');
 INSERT INTO newproducts VALUES (1601, 'lamaze', 'toys');
 INSERT INTO newproducts VALUES (1666, 'harry potter', 'toys');
 INSERT INTO newproducts VALUES (1700, 'wait interface', 'books');


MERGE INTO products p
USING newproducts np
ON (p.product_id = np.product_id)
WHEN MATCHED THEN
  UPDATE SET p.product_name = np.product_name, p.category = np.category WHERE p.product_name != 'play gym'
WHEN NOT MATCHED THEN
  INSERT VALUES (np.product_id, np.product_name, np.category) WHERE np.category = 'books';

SELECT * FROM products ORDER BY product_id;

drop table products;
drop table newproducts;





