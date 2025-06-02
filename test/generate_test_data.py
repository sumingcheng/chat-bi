import asyncio
import logging
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import uuid4
from faker import Faker

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent  # 向上一级到项目根目录
sys.path.insert(0, str(project_root))

from app.database.base import get_business_session, get_system_session
from app.database.business_models import Category, Customer, Product, SalesOrder, OrderItem, Sales
from app.database.system_models import SQLTemplate, SQLTemplateParam, QueryHistory

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Faker
fake = Faker(['zh_CN'])  # 使用中文数据
Faker.seed(42)  # 设置随机种子，保证数据可复现

class TestDataGenerator:
    def __init__(self):
        self.categories = []
        self.customers = []
        self.products = []
        self.orders = []
        
    async def generate_categories(self, session, count=20):
        """生成产品分类数据"""
        categories = [
            "电子产品", "服装配饰", "家居用品", "美妆护肤", "运动户外",
            "图书文教", "母婴用品", "食品饮料", "汽车用品", "医疗保健",
            "珠宝首饰", "玩具乐器", "宠物用品", "办公用品", "工具五金",
            "数码配件", "家用电器", "建材装修", "农资园艺", "礼品收藏"
        ]
        
        for i, name in enumerate(categories):
            category = Category(
                category_name=name,
                category_description=f"{name}相关商品分类，包含各种优质{name}商品"
            )
            session.add(category)
            self.categories.append(category)
        
        await session.commit()
        logger.info(f"✓ 生成了 {len(categories)} 条分类数据")
        
    async def generate_customers(self, session, count=200):
        """生成客户数据"""
        for i in range(count):
            customer = Customer(
                username=fake.user_name() + str(i),
                email=f"{fake.user_name()}{i}@{fake.free_email_domain()}",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                registration_date=fake.date_time_between(start_date='-2y', end_date='now'),
                account_status=random.choice(['active', 'inactive'])
            )
            session.add(customer)
            self.customers.append(customer)
        
        await session.commit()
        logger.info(f"✓ 生成了 {count} 条客户数据")
        
    async def generate_products(self, session, count=100):
        """生成产品数据"""
        for i in range(count):
            category = random.choice(self.categories)
            product = Product(
                product_name=fake.catch_phrase() + f" {category.category_name}商品",
                category_id=category.category_id,
                product_description=fake.text(max_nb_chars=200),
                price=Decimal(str(random.uniform(10.00, 9999.99))).quantize(Decimal('0.01')),
                stock_quantity=random.randint(0, 1000),
                created_at=fake.date_time_between(start_date='-1y', end_date='now'),
                updated_at=fake.date_time_between(start_date='-6m', end_date='now')
            )
            session.add(product)
            self.products.append(product)
        
        await session.commit()
        logger.info(f"✓ 生成了 {count} 条产品数据")
        
    async def generate_orders_and_items(self, session, order_count=300):
        """生成订单和订单项数据"""
        order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        for i in range(order_count):
            customer = random.choice(self.customers)
            order = SalesOrder(
                customer_id=customer.customer_id,
                order_date=fake.date_time_between(start_date='-1y', end_date='now'),
                total_amount=Decimal('0.00'),
                order_status=random.choice(order_statuses),
                shipping_address=fake.address(),
                notes=fake.text(max_nb_chars=100) if random.random() > 0.7 else None
            )
            session.add(order)
            await session.flush()  # 获取order_id
            
            # 为每个订单生成1-5个订单项
            items_count = random.randint(1, 5)
            total_amount = Decimal('0.00')
            
            for j in range(items_count):
                product = random.choice(self.products)
                quantity = random.randint(1, 10)
                unit_price = product.price * Decimal(str(random.uniform(0.8, 1.2))).quantize(Decimal('0.01'))
                
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=product.product_id,
                    quantity=quantity,
                    unit_price=unit_price
                )
                session.add(order_item)
                total_amount += unit_price * quantity
            
            order.total_amount = total_amount
            self.orders.append(order)
        
        await session.commit()
        logger.info(f"✓ 生成了 {order_count} 条订单数据及相关订单项")
        
    async def generate_sales(self, session, count=400):
        """生成销售记录数据"""
        for i in range(count):
            customer = random.choice(self.customers)
            product = random.choice(self.products)
            quantity = random.randint(1, 20)
            
            sale = Sales(
                product_id=product.product_id,
                customer_id=customer.customer_id,
                quantity=quantity,
                total_amount=product.price * quantity,
                sale_date=fake.date_time_between(start_date='-1y', end_date='now')
            )
            session.add(sale)
        
        await session.commit()
        logger.info(f"✓ 生成了 {count} 条销售记录")
        
    async def generate_sql_templates(self, session, count=20):
        """生成SQL模板数据"""
        templates = [
            {
                "description": "查询客户订单统计",
                "sql_text": "SELECT c.username, COUNT(o.order_id) as order_count, SUM(o.total_amount) as total_spent FROM customer c LEFT JOIN sales_order o ON c.customer_id = o.customer_id WHERE c.registration_date >= '{start_date}' GROUP BY c.customer_id",
                "scenario": "客户分析",
                "params": [
                    {"param_name": "start_date", "param_description": "开始日期", "param_type": "date"}
                ]
            },
            {
                "description": "产品销量排行榜",
                "sql_text": "SELECT p.product_name, SUM(s.quantity) as total_sold FROM product p JOIN sales s ON p.product_id = s.product_id WHERE s.sale_date >= '{start_date}' GROUP BY p.product_id ORDER BY total_sold DESC LIMIT {limit}",
                "scenario": "产品分析",
                "params": [
                    {"param_name": "start_date", "param_description": "开始日期", "param_type": "date"},
                    {"param_name": "limit", "param_description": "返回数量", "param_type": "integer"}
                ]
            },
            {
                "description": "每月销售趋势",
                "sql_text": "SELECT DATE_FORMAT(sale_date, '%Y-%m') as month, SUM(total_amount) as monthly_sales FROM sales WHERE sale_date >= '{start_date}' GROUP BY DATE_FORMAT(sale_date, '%Y-%m') ORDER BY month",
                "scenario": "趋势分析",
                "params": [
                    {"param_name": "start_date", "param_description": "开始日期", "param_type": "date"}
                ]
            },
            {
                "description": "分类销售统计",
                "sql_text": "SELECT c.category_name, COUNT(DISTINCT p.product_id) as product_count, SUM(s.total_amount) as category_sales FROM category c JOIN product p ON c.category_id = p.category_id JOIN sales s ON p.product_id = s.product_id GROUP BY c.category_id ORDER BY category_sales DESC",
                "scenario": "分类分析",
                "params": []
            },
            {
                "description": "高价值客户识别",
                "sql_text": "SELECT c.username, c.email, SUM(s.total_amount) as total_spent FROM customer c JOIN sales s ON c.customer_id = s.customer_id GROUP BY c.customer_id HAVING total_spent > {min_amount} ORDER BY total_spent DESC",
                "scenario": "客户分析",
                "params": [
                    {"param_name": "min_amount", "param_description": "最小消费金额", "param_type": "decimal"}
                ]
            }
        ]
        
        for template_data in templates:
            template = SQLTemplate(
                description=template_data["description"],
                sql_text=template_data["sql_text"],
                scenario=template_data["scenario"],
                created_at=fake.date_time_between(start_date='-1y', end_date='now'),
                updated_at=fake.date_time_between(start_date='-6m', end_date='now')
            )
            session.add(template)
            await session.flush()
            
            # 添加参数
            for param_data in template_data["params"]:
                param = SQLTemplateParam(
                    template_id=template.id,
                    param_name=param_data["param_name"],
                    param_description=param_data["param_description"],
                    param_type=param_data["param_type"]
                )
                session.add(param)
        
        await session.commit()
        logger.info(f"✓ 生成了 {len(templates)} 条SQL模板数据")
        
    async def generate_query_history(self, session, count=100):
        """生成查询历史数据"""
        satisfaction_levels = ['satisfied', 'neutral', 'unsatisfied']
        visualization_types = ['table', 'chart', 'graph', 'pie', 'bar']
        
        sample_queries = [
            "显示最近一个月的销售情况",
            "哪些产品最受欢迎？",
            "客户消费排行榜",
            "各个分类的销售占比",
            "订单状态分布情况",
            "库存不足的产品有哪些？",
            "新注册客户数量趋势",
            "平均订单金额是多少？",
            "退货率最高的产品",
            "销售额增长趋势"
        ]
        
        for i in range(count):
            query_history = QueryHistory(
                query_id=str(uuid4()),
                user_input=random.choice(sample_queries) + f" - 查询{i+1}",
                sql_query=f"SELECT * FROM sales WHERE sale_date >= '2023-01-01' LIMIT {random.randint(10, 100)}",
                result=f"查询返回 {random.randint(1, 500)} 条记录",
                satisfaction_level=random.choice(satisfaction_levels),
                visualization_type=random.choice(visualization_types),
                created_at=fake.date_time_between(start_date='-6m', end_date='now')
            )
            session.add(query_history)
        
        await session.commit()
        logger.info(f"✓ 生成了 {count} 条查询历史数据")

async def main():
    """主函数"""
    logger.info("🚀 开始生成测试数据...")
    generator = TestDataGenerator()
    
    try:
        # 生成业务数据
        async for business_session in get_business_session():
            logger.info("📊 生成业务数据...")
            await generator.generate_categories(business_session)
            await generator.generate_customers(business_session, 200)
            await generator.generate_products(business_session, 100)
            await generator.generate_orders_and_items(business_session, 300)
            await generator.generate_sales(business_session, 400)
            break
        
        # 生成系统数据
        async for system_session in get_system_session():
            logger.info("⚙️ 生成系统数据...")
            await generator.generate_sql_templates(system_session, 20)
            await generator.generate_query_history(system_session, 100)
            break
        
        logger.info("✅ 测试数据生成完成！")
        logger.info("📈 数据统计:")
        logger.info("  - 分类数据: 20 条")
        logger.info("  - 客户数据: 200 条") 
        logger.info("  - 产品数据: 100 条")
        logger.info("  - 订单数据: 300 条 (包含订单项)")
        logger.info("  - 销售记录: 400 条")
        logger.info("  - SQL模板: 20 条")
        logger.info("  - 查询历史: 100 条")
        logger.info("  - 总计: 1000+ 条测试数据")
        
    except Exception as e:
        logger.error(f"❌ 生成测试数据失败: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 