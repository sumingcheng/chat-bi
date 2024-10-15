use chat_bi;
-- 创建 products 表
CREATE TABLE products
(
    id   INT PRIMARY KEY,
    name VARCHAR(255)
);

-- 创建 sales 表
CREATE TABLE sales
(
    id         INT PRIMARY KEY,
    product_id INT,
    amount     DECIMAL(10, 2),
    date       DATE,
    FOREIGN KEY (product_id) REFERENCES products (id)
);

-- 插入示例数据到 products 表
INSERT INTO products (id, name)
VALUES (1, '产品A'),
       (2, '产品B'),
       (3, '产品C');

-- 插入示例数据到 sales 表
INSERT INTO sales (id, product_id, amount, date)
VALUES (1, 1, 100.00, '2014-01-15'),
       (2, 2, 200.00, '2014-05-23'),
       (3, 1, 150.00, '2015-03-12'),
       (4, 3, 300.00, '2014-07-19'),
       (5, 2, 250.00, '2015-11-30');
