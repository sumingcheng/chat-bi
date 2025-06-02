from .base import Base
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class SQLTemplate(Base):
    __tablename__ = 'sql_templates'
    
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    sql_text = Column(Text, nullable=False)
    scenario = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    params = relationship("SQLTemplateParam", back_populates="template", cascade="all, delete-orphan")


class SQLTemplateParam(Base):
    __tablename__ = 'sql_template_params'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('sql_templates.id', ondelete='CASCADE'), nullable=False)
    param_name = Column(String(100), nullable=False)
    param_description = Column(Text)
    param_type = Column(String(50), nullable=False)
    
    template = relationship("SQLTemplate", back_populates="params")


class QueryHistory(Base):
    __tablename__ = 'query_history'
    
    query_id = Column(String(36), primary_key=True)
    user_input = Column(Text, nullable=False)
    sql_query = Column(Text)
    result = Column(Text)
    satisfaction_level = Column(Enum('satisfied', 'neutral', 'unsatisfied', name='satisfaction_enum'))
    visualization_type = Column(String(50), server_default='table')
    created_at = Column(DateTime, server_default=func.now()) 