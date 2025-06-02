# Chat-BI 测试数据生成工具

## 📋 概述

此工具为 Chat-BI 项目生成完整的测试数据集，包含 1000+ 条模拟业务数据，用于开发、测试和演示。

## 📊 生成的数据

### 业务数据 (1020 条)
- **分类数据**: 20 条 - 电子产品、服装配饰、家居用品等分类
- **客户数据**: 200 条 - 包含用户名、邮箱、电话、注册日期等
- **产品数据**: 100 条 - 每个分类下的商品，包含价格、库存、描述等
- **订单数据**: 300 条 - 订单信息及相关订单项（每订单1-5个商品）
- **销售记录**: 400 条 - 销售流水记录

### 系统数据 (120 条)
- **SQL模板**: 20 条 - 预设的查询模板及参数
- **查询历史**: 100 条 - 模拟的用户查询记录

## 🚀 使用方法

### 方式1: 一键运行（推荐）
```bash
# 在项目根目录下运行
python test/run_test_data.py

# 或者进入test目录运行
cd test
python run_test_data.py
```

### 方式2: 手动运行
```bash
# 1. 安装依赖
pip install faker>=30.5.0

# 2. 运行生成脚本（在项目根目录）
python test/generate_test_data.py

# 或者进入test目录运行
cd test
python generate_test_data.py
```

## 📁 文件说明

- `test/generate_test_data.py` - 主要的数据生成脚本
- `test/run_test_data.py` - 一键运行脚本（包含依赖安装）
- `test/TEST_DATA_README.md` - 此说明文档

## ⚙️ 前置条件

1. **数据库配置**: 确保 `.env` 文件中的数据库配置正确
2. **数据库表**: 运行前需要先创建数据库表结构：
   ```bash
   python app/database/init_db.py
   ```
3. **Python环境**: Python 3.10+

## 📝 数据特点

- **真实性**: 使用 Faker 库生成符合中国本土化的模拟数据
- **关联性**: 数据之间保持合理的外键关联关系
- **多样性**: 涵盖各种业务场景，状态分布合理
- **时间跨度**: 数据时间跨度覆盖过去1-2年

## 🔍 数据验证

生成完成后，可以通过以下方式验证数据：

```sql
-- 检查数据量
SELECT 'categories' as table_name, COUNT(*) as count FROM category
UNION ALL
SELECT 'customers', COUNT(*) FROM customer
UNION ALL  
SELECT 'products', COUNT(*) FROM product
UNION ALL
SELECT 'orders', COUNT(*) FROM sales_order
UNION ALL
SELECT 'sales', COUNT(*) FROM sales;
```

## 🎯 使用场景

1. **开发测试**: 为开发环境提供充足的测试数据
2. **性能测试**: 评估系统在有数据情况下的性能表现  
3. **功能演示**: 为产品演示提供丰富的示例数据
4. **AI训练**: 为Chat-BI的自然语言处理提供训练素材

## ⚠️ 注意事项

- 生成过程中会自动设置随机种子(42)，确保数据可复现
- 请确保数据库有足够的存储空间
- 建议在开发/测试环境中使用，避免在生产环境运行
- 每次运行会清空并重新生成数据（如果需要保留现有数据，请先备份）

## 🛠️ 自定义选项

可以通过修改 `generate_test_data.py` 中的参数来调整生成的数据量：

```python
# 在 main() 函数中调整以下参数
await generator.generate_customers(business_session, 200)  # 客户数量
await generator.generate_products(business_session, 100)   # 产品数量  
await generator.generate_orders_and_items(business_session, 300)  # 订单数量
await generator.generate_sales(business_session, 400)     # 销售记录数量
```

## 📞 支持

如遇到问题，请检查：
1. 数据库连接配置是否正确
2. 依赖库是否已安装
3. 数据库表结构是否已创建
4. 查看生成脚本的错误日志 