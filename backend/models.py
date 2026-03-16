from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    brief = Column(Text, nullable=False)
    code = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), default="active")  # active, completed, archived
    phase = Column(String(30), default="planning")  # planning, development, testing, deployment
    agent_outputs = Column(Text, default="{}")  # JSON string
    quality_score = Column(Float, default=0.0)  # 0-100 arası kalite skoru
    cost = Column(Float, default=0.0)  # Maliyet