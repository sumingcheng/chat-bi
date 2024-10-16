use chat_bi;

-- 如果存在则删除已有的表（注意：在生产环境中要谨慎执行此操作）
drop table if exists sales;
drop table if exists order_item;
drop table if exists sales_order;
drop table if exists customer;
drop table if exists product;
drop table if exists category;