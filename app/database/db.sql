USE chat_bi;

-- 创建 category（产品类别）表
CREATE TABLE category
(
    category_id          INT AUTO_INCREMENT PRIMARY KEY COMMENT '类别ID',
    category_name        VARCHAR(255) NOT NULL COMMENT '类别名称',
    category_description TEXT COMMENT '类别描述'
) COMMENT ='产品类别表';

-- 创建 customer（客户）表
CREATE TABLE customer
(
    customer_id       INT AUTO_INCREMENT PRIMARY KEY COMMENT '客户ID',
    username          VARCHAR(50)  NOT NULL UNIQUE COMMENT '用户名',
    password_hash     VARCHAR(255) NOT NULL COMMENT '密码哈希值',
    email             VARCHAR(255) NOT NULL UNIQUE COMMENT '电子邮箱',
    first_name        VARCHAR(50) COMMENT '名',
    last_name         VARCHAR(50) COMMENT '姓',
    date_of_birth     DATE COMMENT '出生日期',
    registration_date DATETIME                              DEFAULT CURRENT_TIMESTAMP COMMENT '注册日期',
    last_login        DATETIME COMMENT '最后登录时间',
    account_status    ENUM ('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '账号状态'
) COMMENT ='客户信息表';

-- 创建 product（产品）表
CREATE TABLE product
(
    product_id          INT AUTO_INCREMENT PRIMARY KEY COMMENT '产品ID',
    product_name        VARCHAR(255)   NOT NULL COMMENT '产品名称',
    category_id         INT COMMENT '类别ID',
    product_description TEXT COMMENT '产品描述',
    price               DECIMAL(10, 2) NOT NULL COMMENT '价格',
    stock_quantity      INT      DEFAULT 0 COMMENT '库存数量',
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (category_id) REFERENCES category (category_id)
) COMMENT ='产品信息表';

-- 创建 sales_order（销售订单）表
CREATE TABLE sales_order
(
    order_id         INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    customer_id      INT COMMENT '客户ID',
    order_date       DATETIME                                                            DEFAULT CURRENT_TIMESTAMP COMMENT '订单日期',
    total_amount     DECIMAL(10, 2) COMMENT '总金额',
    order_status     ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending' COMMENT '订单状态',
    shipping_address VARCHAR(255) COMMENT '收货地址',
    billing_address  VARCHAR(255) COMMENT '账单地址',
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
) COMMENT ='销售订单表';

-- 创建 order_item（订单项）表
CREATE TABLE order_item
(
    order_item_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单项ID',
    order_id      INT COMMENT '订单ID',
    product_id    INT COMMENT '产品ID',
    quantity      INT            NOT NULL COMMENT '购买数量',
    unit_price    DECIMAL(10, 2) NOT NULL COMMENT '单价',
    FOREIGN KEY (order_id) REFERENCES sales_order (order_id),
    FOREIGN KEY (product_id) REFERENCES product (product_id)
) COMMENT ='订单项表';

-- 创建 sales（销售记录）表
CREATE TABLE sales
(
    sale_id      INT AUTO_INCREMENT PRIMARY KEY COMMENT '销售ID',
    product_id   INT COMMENT '产品ID',
    customer_id  INT COMMENT '客户ID',
    quantity     INT            NOT NULL COMMENT '销售数量',
    total_amount DECIMAL(10, 2) NOT NULL COMMENT '销售总额',
    sale_date    DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '销售日期',
    FOREIGN KEY (product_id) REFERENCES product (product_id),
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
) COMMENT ='销售记录表';

INSERT INTO category (category_name, category_description)
VALUES ('电子产品', '电子设备和配件'),
       ('图书', '纸质和电子书籍'),
       ('服装', '男装和女装'),
       ('家居用品', '家庭和厨房用品');

INSERT INTO customer (username, password_hash, email, first_name, last_name, date_of_birth, registration_date,
                      last_login, account_status)
VALUES ('john_doe', 'hashed_password1', 'john@example.com', '约翰', '多伊', '1985-05-15', '2024-01-10', '2024-10-15',
        'active'),
       ('jane_smith', 'hashed_password2', 'jane@example.com', '简', '史密斯', '1990-08-22', '2024-02-20', '2024-10-12',
        'active'),
       ('alice_wong', 'hashed_password3', 'alice@example.com', '爱丽丝', '王', '1992-12-05', '2024-03-15', '2024-10-10',
        'active'),
       ('bob_brown', 'hashed_password4', 'bob@example.com', '鲍勃', '布朗', '1988-07-30', '2024-04-18', '2024-10-08',
        'inactive'),
       ('charlie_lee', 'hashed_password5', 'charlie@example.com', '查理', '李', '1995-09-12', '2024-05-22',
        '2024-10-05', 'active'),
       ('diana_clark', 'hashed_password6', 'diana@example.com', '戴安娜', '克拉克', '1993-11-03', '2024-06-18',
        '2024-10-03', 'active');

INSERT INTO product (product_name, category_id, product_description, price, stock_quantity)
VALUES ('智能手机 XYZ', 1, '最新款智能手机，具备高级功能', 699.99, 50),
       ('笔记本电脑 ABC', 1, '高性能笔记本电脑，适合游戏和专业工作', 1299.99, 30),
       ('小说《伟大的冒险》', 2, '一部关于冒险和发现的惊险小说', 19.99, 100),
       ('男士 T 恤', 3, '舒适的纯棉男士 T 恤', 14.99, 200),
       ('专业搅拌机', 4, '高速搅拌机，适合制作奶昔和汤品', 89.99, 40),
       ('无线耳机', 1, '降噪无线耳机，电池续航时间长', 149.99, 80),
       ('电子书阅读器', 1, '轻便的电子书阅读器，高清显示屏', 129.99, 60),
       ('食谱《健康食谱》', 2, '一本健康美味的食谱合集', 29.99, 120),
       ('女士牛仔裤', 3, '时尚舒适的女士牛仔裤', 49.99, 150),
       ('咖啡机', 4, '可编程设置的全自动咖啡机', 79.99, 70),
       ('游戏机', 1, '次世代游戏机，享受沉浸式游戏体验', 499.99, 40),
       ('无线鼠标', 1, '人体工学无线鼠标，DPI 可调节', 24.99, 100),
       ('儿童故事书', 2, '适合儿童阅读的插画故事书', 9.99, 200),
       ('健身追踪器', 1, '可穿戴健身追踪器，心率监测功能', 59.99, 90),
       ('搅拌杯', 4, '便携式搅拌杯，适合制作蛋白奶昔', 19.99, 150),
       ('厨房刀具套装', 4, '不锈钢厨房刀具，配木制刀架', 99.99, 50),
       ('女士连衣裙', 3, '优雅的晚礼连衣裙，适合特殊场合', 89.99, 80),
       ('男士运动鞋', 3, '舒适时尚的男士运动鞋', 69.99, 120),
       ('台灯', 4, 'LED 台灯，可调节亮度', 39.99, 60),
       ('降噪耳机', 1, '头戴式主动降噪耳机', 199.99, 35);

INSERT INTO sales_order (customer_id, order_date, total_amount, order_status, shipping_address, billing_address)
VALUES (1, '2024-10-01 10:15:00', 719.98, 'delivered', '城市 A，主街 123 号', '城市 A，主街 123 号'),
       (2, '2024-10-05 14:30:00', 19.99, 'shipped', '城市 B，橡树大道 456 号', '城市 B，橡树大道 456 号'),
       (3, '2024-10-07 09:45:00', 104.98, 'processing', '城市 C，松树路 789 号', '城市 C，松树路 789 号'),
       (4, '2024-10-09 11:20:00', 549.97, 'pending', '城市 D，枫树街 101 号', '城市 D，枫树街 101 号'),
       (5, '2024-10-12 16:05:00', 299.97, 'delivered', '城市 E，桦树大道 202 号', '城市 E，桦树大道 202 号'),
       (6, '2024-10-15 13:50:00', 99.98, 'processing', '城市 F，柳树巷 303 号', '城市 F，柳树巷 303 号'),
       (1, '2024-10-17 08:30:00', 159.97, 'shipped', '城市 A，主街 123 号', '城市 A，主街 123 号'),
       (2, '2024-10-18 14:10:00', 49.99, 'cancelled', '城市 B，橡树大道 456 号', '城市 B，橡树大道 456 号'),
       (3, '2024-10-20 10:25:00', 269.97, 'delivered', '城市 C，松树路 789 号', '城市 C，松树路 789 号'),
       (4, '2024-10-22 15:40:00', 199.99, 'pending', '城市 D，枫树街 101 号', '城市 D，枫树街 101 号');

INSERT INTO order_item (order_id, product_id, quantity, unit_price)
VALUES (1, 1, 1, 699.99),
       (1, 5, 1, 19.99),
       (2, 3, 1, 19.99),
       (3, 4, 2, 14.99),
       (3, 5, 1, 74.99),
       (4, 2, 1, 1299.99),
       (4, 6, 2, 149.99),
       (5, 9, 3, 49.99),
       (6, 8, 2, 29.99),
       (6, 13, 1, 9.99),
       (7, 14, 1, 59.99),
       (7, 15, 5, 19.99),
       (8, 10, 3, 79.99),
       (9, 20, 1, 199.99),
       (10, 7, 1, 129.99),
       (5, 5, 2, 89.99),
       (5, 16, 1, 99.99),
       (9, 18, 2, 69.99),
       (10, 19, 1, 39.99),
       (4, 17, 1, 89.99);

INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date)
VALUES (1, 1, 1, 699.99, '2024-10-01 10:15:00'),
       (5, 1, 1, 19.99, '2024-10-01 10:15:00'),
       (3, 2, 1, 19.99, '2024-10-05 14:30:00'),
       (4, 3, 2, 29.98, '2024-10-07 09:45:00'),
       (5, 3, 1, 74.99, '2024-10-07 09:45:00'),
       (2, 4, 1, 1299.99, '2024-10-09 11:20:00'),
       (6, 4, 2, 299.98, '2024-10-09 11:20:00'),
       (9, 5, 3, 149.97, '2024-10-12 16:05:00'),
       (8, 6, 2, 59.98, '2024-10-15 13:50:00'),
       (13, 6, 1, 9.99, '2024-10-15 13:50:00'),
       (14, 1, 1, 59.99, '2024-10-17 08:30:00'),
       (15, 1, 5, 99.95, '2024-10-17 08:30:00'),
       (10, 3, 3, 239.97, '2024-10-20 10:25:00'),
       (7, 4, 1, 129.99, '2024-10-22 15:40:00'),
       (16, 5, 1, 99.99, '2024-10-12 16:05:00'),
       (17, 4, 1, 89.99, '2024-10-22 15:40:00'),
       (18, 4, 2, 139.98, '2024-10-22 15:40:00'),
       (19, 4, 1, 39.99, '2024-10-22 15:40:00'),
       (20, 3, 1, 199.99, '2024-10-18 14:10:00'),
       (8, 3, 1, 29.99, '2024-10-18 14:10:00');
