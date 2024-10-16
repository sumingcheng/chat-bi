USE chat_bi;

-- 如果存在则删除已有的表（注意：在生产环境中要谨慎执行此操作）
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS sales_order;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;