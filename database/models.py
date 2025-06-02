from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import Optional

Base = declarative_base()

class SQLTemplate(Base):
    __tablename__ = 'sql_templates'
    
    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)
    sql_text = Column(Text, nullable=False)
    scenario = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class SQLTemplateParam(Base):
    __tablename__ = 'sql_template_params'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('sql_templates.id', ondelete='CASCADE'))
    param_name = Column(String(100), nullable=False)
    param_description = Column(Text)
    param_type = Column(String(50), nullable=False)

class QueryHistory(Base):
    __tablename__ = 'query_history'
    
    query_id = Column(String(36), primary_key=True)
    user_input = Column(Text, nullable=False)
    sql_query = Column(Text)
    result = Column(Text)
    satisfaction_level = Column(Enum('satisfied', 'neutral', 'unsatisfied'))
    visualization_type = Column(String(50), server_default='table')
    created_at = Column(DateTime, server_default=func.now()) 