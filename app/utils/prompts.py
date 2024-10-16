database_schema = """
DDL for category:
CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT COMMENT '类别ID',
  `category_name` varchar(255) NOT NULL COMMENT '类别名称',
  `category_description` text COMMENT '类别描述',
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品类别表'

DDL for customer:
CREATE TABLE `customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT COMMENT '客户ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password_hash` varchar(255) NOT NULL COMMENT '密码哈希值',
  `email` varchar(255) NOT NULL COMMENT '电子邮箱',
  `first_name` varchar(50) DEFAULT NULL COMMENT '名',
  `last_name` varchar(50) DEFAULT NULL COMMENT '姓',
  `date_of_birth` date DEFAULT NULL COMMENT '出生日期',
  `registration_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '注册日期',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `account_status` enum('active','inactive','banned') DEFAULT 'active' COMMENT '账号状态',
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='客户信息表'

DDL for order_item:
CREATE TABLE `order_item` (
  `order_item_id` int NOT NULL AUTO_INCREMENT COMMENT '订单项ID',
  `order_id` int DEFAULT NULL COMMENT '订单ID',
  `product_id` int DEFAULT NULL COMMENT '产品ID',
  `quantity` int NOT NULL COMMENT '购买数量',
  `unit_price` decimal(10,2) NOT NULL COMMENT '单价',
  PRIMARY KEY (`order_item_id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `sales_order` (`order_id`),
  CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单项表'

DDL for product:
CREATE TABLE `product` (
  `product_id` int NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `product_name` varchar(255) NOT NULL COMMENT '产品名称',
  `category_id` int DEFAULT NULL COMMENT '类别ID',
  `product_description` text COMMENT '产品描述',
  `price` decimal(10,2) NOT NULL COMMENT '价格',
  `stock_quantity` int DEFAULT '0' COMMENT '库存数量',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`product_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='产品信息表'

DDL for sales:
CREATE TABLE `sales` (
  `sale_id` int NOT NULL AUTO_INCREMENT COMMENT '销售ID',
  `product_id` int DEFAULT NULL COMMENT '产品ID',
  `customer_id` int DEFAULT NULL COMMENT '客户ID',
  `quantity` int NOT NULL COMMENT '销售数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '销售总额',
  `sale_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '销售日期',
  PRIMARY KEY (`sale_id`),
  KEY `product_id` (`product_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='销售记录表'

DDL for sales_order:
CREATE TABLE `sales_order` (
  `order_id` int NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `customer_id` int DEFAULT NULL COMMENT '客户ID',
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '订单日期',
  `total_amount` decimal(10,2) DEFAULT NULL COMMENT '总金额',
  `order_status` enum('pending','processing','shipped','delivered','cancelled') DEFAULT 'pending' COMMENT '订单状态',
  `shipping_address` varchar(255) DEFAULT NULL COMMENT '收货地址',
  `billing_address` varchar(255) DEFAULT NULL COMMENT '账单地址',
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `sales_order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='销售订单表'
"""
