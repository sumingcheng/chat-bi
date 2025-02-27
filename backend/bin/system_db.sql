-- 创建系统数据库
DROP DATABASE IF EXISTS query_sys;

CREATE DATABASE query_sys;

USE query_sys;

-- 创建SQL模板表
CREATE TABLE
  IF NOT EXISTS sql_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL COMMENT '模板描述',
    sql_text TEXT NOT NULL COMMENT 'SQL模板文本',
    scenario VARCHAR(255) NOT NULL COMMENT '适用场景',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'SQL模板表';

-- 创建SQL模板参数表
CREATE TABLE
  IF NOT EXISTS sql_template_params (
    id INT AUTO_INCREMENT PRIMARY KEY,
    template_id INT NOT NULL COMMENT '模板ID',
    param_name VARCHAR(100) NOT NULL COMMENT '参数名',
    param_description TEXT COMMENT '参数描述',
    param_type VARCHAR(50) NOT NULL COMMENT '参数类型',
    FOREIGN KEY (template_id) REFERENCES sql_templates (id) ON DELETE CASCADE
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = 'SQL模板参数表';

-- 创建查询历史表
CREATE TABLE
  IF NOT EXISTS query_history (
    query_id VARCHAR(36) PRIMARY KEY COMMENT '查询ID',
    user_input TEXT NOT NULL COMMENT '用户输入',
    sql_query TEXT COMMENT 'SQL查询',
    result TEXT COMMENT '查询结果',
    satisfaction_level ENUM ('satisfied', 'neutral', 'unsatisfied') COMMENT '满意度',
    visualization_type VARCHAR(50) DEFAULT 'table' COMMENT '可视化类型',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '查询历史表';

-- 添加索引
CREATE INDEX idx_query_history_created_at ON query_history (created_at);

CREATE INDEX idx_template_params_template_id ON sql_template_params (template_id);

-- 插入测试数据
INSERT INTO
  sql_templates (description, sql_text, scenario)
VALUES
  (
    '按时间范围统计销售额',
    'SELECT DATE(sale_date) as date, SUM(total_amount) as daily_sales FROM sales WHERE sale_date BETWEEN {start_date} AND {end_date} GROUP BY DATE(sale_date) ORDER BY date',
    '销售额统计'
  );

-- 插入模板参数
INSERT INTO
  sql_template_params (
    template_id,
    param_name,
    param_description,
    param_type
  )
VALUES
  (1, 'start_date', '开始日期', 'date'),
  (1, 'end_date', '结束日期', 'date');

-- 插入一条查询历史记录
INSERT INTO
  query_history (
    query_id,
    user_input,
    sql_query,
    result,
    satisfaction_level,
    visualization_type
  )
VALUES
  (
    'test-query-001',
    '查询最近一周的每日销售额',
    'SELECT DATE(sale_date) as date, SUM(total_amount) as daily_sales FROM sales WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY DATE(sale_date)',
    '{"columns":["date","daily_sales"],"data":[["2024-03-10",1500.00],["2024-03-11",2000.00]]}',
    'satisfied',
    'line'
  );