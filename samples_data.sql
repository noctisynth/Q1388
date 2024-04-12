--+ product category
INSERT INTO "main"."product_category" ("id", "name", "description") VALUES ('1', '电子产品', '各种电子产品');
INSERT INTO "main"."product_category" ("id", "name", "description") VALUES ('2', '服装', '各种服装');
INSERT INTO "main"."product_category" ("id", "name", "description") VALUES ('3', '图书', '各种图书');
--+ product
INSERT INTO "main"."product_product" ("id", "name", "price", "quantity", "spec_param", "comment", "detail", "pictures") VALUES ('1', '手机', '1000', '10', '4G手机', '很好用的手机', '这是一个很好用的手机', 'phone.jpg');
INSERT INTO "main"."product_product" ("id", "name", "price", "quantity", "spec_param", "comment", "detail", "pictures") VALUES ('2', 'T恤', '20', '50', '纯棉T恤', '舒适的T恤', '这是一件舒适的T恤', 'tshirt.jpg');
INSERT INTO "main"."product_product" ("id", "name", "price", "quantity", "spec_param", "comment", "detail", "pictures") VALUES ('3', 'Python编程入门', '50', '30', 'Python编程入门书籍', '学习编程的好书', '这是一本Python编程入门的好书', 'book.jpg');
--+ product categories data
INSERT INTO "main"."product_product_categories" ("id", "product_id", "category_id") VALUES ('1', '1', '1');
INSERT INTO "main"."product_product_categories" ("id", "product_id", "category_id") VALUES ('2', '2', '2');
INSERT INTO "main"."product_product_categories" ("id", "product_id", "category_id") VALUES ('3', '3', '3');
