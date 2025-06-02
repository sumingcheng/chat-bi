from .base import Base
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, DECIMAL, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'category'
    
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)
    category_description = Column(Text)
    
    products = relationship("Product", back_populates="category")


class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    registration_date = Column(DateTime, server_default=func.now())
    account_status = Column(Enum('active', 'inactive', name='account_status_enum'), server_default='active')
    
    orders = relationship("SalesOrder", back_populates="customer")
    sales = relationship("Sales", back_populates="customer")


class Product(Base):
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    product_description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, server_default='0')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    sales = relationship("Sales", back_populates="product")
    
    __table_args__ = (Index('idx_product_price', 'price'),)


class SalesOrder(Base):
    __tablename__ = 'sales_order'
    
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    order_date = Column(DateTime, server_default=func.now())
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    order_status = Column(
        Enum('pending', 'processing', 'shipped', 'delivered', 'cancelled', name='order_status_enum'),
        server_default='pending'
    )
    shipping_address = Column(Text)
    notes = Column(Text)
    
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = 'order_item'
    
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('sales_order.order_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    
    order = relationship("SalesOrder", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    __table_args__ = (Index('idx_order_product', 'order_id', 'product_id'),)


class Sales(Base):
    __tablename__ = 'sales'
    
    sale_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    sale_date = Column(DateTime, server_default=func.now())
    
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    
    __table_args__ = (Index('idx_sale_date', 'sale_date'),) 