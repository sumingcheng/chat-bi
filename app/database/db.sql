-- 切换到数据库
use chat_bi;

-- 创建 category（产品类别）表
create table category
(
    category_id          int auto_increment primary key comment '类别ID',
    category_name        varchar(255) not null comment '类别名称',
    category_description text comment '类别描述'
) comment ='产品类别表';

-- 创建 customer（客户）表
create table customer
(
    customer_id       int auto_increment primary key comment '客户ID',
    username          varchar(50)  not null unique comment '用户名',
    password_hash     varchar(255) not null comment '密码哈希值',
    email             varchar(255) not null unique comment '电子邮箱',
    first_name        varchar(50) comment '名',
    last_name         varchar(50) comment '姓',
    date_of_birth     date comment '出生日期',
    registration_date datetime                              default current_timestamp comment '注册日期',
    last_login        datetime comment '最后登录时间',
    account_status    enum ('active', 'inactive', 'banned') default 'active' comment '账号状态'
) comment ='客户信息表';

-- 创建 product（产品）表
create table product
(
    product_id          int auto_increment primary key comment '产品ID',
    product_name        varchar(255)   not null comment '产品名称',
    category_id         int comment '类别ID',
    product_description text comment '产品描述',
    price               decimal(10, 2) not null comment '价格',
    stock_quantity      int      default 0 comment '库存数量',
    created_at          datetime default current_timestamp comment '创建时间',
    updated_at          datetime default current_timestamp on update current_timestamp comment '更新时间',
    foreign key (category_id) references category (category_id)
) comment ='产品信息表';

-- 创建 sales_order（销售订单）表
create table sales_order
(
    order_id         int auto_increment primary key comment '订单ID',
    customer_id      int comment '客户ID',
    order_date       datetime                                                            default current_timestamp comment '订单日期',
    total_amount     decimal(10, 2) comment '总金额',
    order_status     enum ('pending', 'processing', 'shipped', 'delivered', 'cancelled') default 'pending' comment '订单状态',
    shipping_address varchar(255) comment '收货地址',
    billing_address  varchar(255) comment '账单地址',
    foreign key (customer_id) references customer (customer_id)
) comment ='销售订单表';

-- 创建 order_item（订单项）表
create table order_item
(
    order_item_id int auto_increment primary key comment '订单项ID',
    order_id      int comment '订单ID',
    product_id    int comment '产品ID',
    quantity      int            not null comment '购买数量',
    unit_price    decimal(10, 2) not null comment '单价',
    foreign key (order_id) references sales_order (order_id),
    foreign key (product_id) references product (product_id)
) comment ='订单项表';

-- 创建 sales（销售记录）表
create table sales
(
    sale_id      int auto_increment primary key comment '销售ID',
    product_id   int comment '产品ID',
    customer_id  int comment '客户ID',
    quantity     int            not null comment '销售数量',
    total_amount decimal(10, 2) not null comment '销售总额',
    sale_date    datetime default current_timestamp comment '销售日期',
    foreign key (product_id) references product (product_id),
    foreign key (customer_id) references customer (customer_id)
) comment ='销售记录表';

insert into category (category_name, category_description)
values ('电子产品', '电子设备和配件'),
       ('图书', '纸质和电子书籍'),
       ('服装', '男装和女装'),
       ('家居用品', '家庭和厨房用品');

insert into customer (username, password_hash, email, first_name, last_name, date_of_birth, registration_date,
                      last_login, account_status)
values ('john_doe', 'hashed_password1', 'john@example.com', '约翰', '多伊', '1985-05-15', '2024-01-10', '2024-10-15',
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

insert into product (product_name, category_id, product_description, price, stock_quantity)
values ('智能手机 XYZ', 1, '最新款智能手机，具备高级功能', 699.99, 50),
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

insert into sales_order (customer_id, order_date, total_amount, order_status, shipping_address, billing_address)
values (1, '2024-10-01 10:15:00', 719.98, 'delivered', '城市 A，主街 123 号', '城市 A，主街 123 号'),
       (2, '2024-10-05 14:30:00', 19.99, 'shipped', '城市 B，橡树大道 456 号', '城市 B，橡树大道 456 号'),
       (3, '2024-10-07 09:45:00', 104.98, 'processing', '城市 C，松树路 789 号', '城市 C，松树路 789 号'),
       (4, '2024-10-09 11:20:00', 549.97, 'pending', '城市 D，枫树街 101 号', '城市 D，枫树街 101 号'),
       (5, '2024-10-12 16:05:00', 299.97, 'delivered', '城市 E，桦树大道 202 号', '城市 E，桦树大道 202 号'),
       (6, '2024-10-15 13:50:00', 99.98, 'processing', '城市 F，柳树巷 303 号', '城市 F，柳树巷 303 号'),
       (1, '2024-10-17 08:30:00', 159.97, 'shipped', '城市 A，主街 123 号', '城市 A，主街 123 号'),
       (2, '2024-10-18 14:10:00', 49.99, 'cancelled', '城市 B，橡树大道 456 号', '城市 B，橡树大道 456 号'),
       (3, '2024-10-20 10:25:00', 269.97, 'delivered', '城市 C，松树路 789 号', '城市 C，松树路 789 号'),
       (4, '2024-10-22 15:40:00', 199.99, 'pending', '城市 D，枫树街 101 号', '城市 D，枫树街 101 号');

insert into order_item (order_id, product_id, quantity, unit_price)
values (1, 1, 1, 699.99),
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

insert into sales (product_id, customer_id, quantity, total_amount, sale_date)
values (1, 1, 1, 699.99, '2024-10-01 10:15:00'),
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
