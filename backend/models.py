from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    product_name = Column(String, nullable=False)
    objective = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="draft")  # draft, pending_approval, approved, rejected, launched, optimized
    
    # Relationships
    segments = relationship("Segment", back_populates="campaign", cascade="all, delete-orphan")
    variants = relationship("Variant", back_populates="campaign", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, product={self.product_name}, status={self.status})>"


class Segment(Base):
    __tablename__ = "segments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    segment_name = Column(String, nullable=False)
    reasoning = Column(Text, nullable=True)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="segments")
    variants = relationship("Variant", back_populates="segment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Segment(id={self.id}, name={self.segment_name})>"


class Variant(Base):
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    segment_id = Column(Integer, ForeignKey("segments.id"), nullable=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    send_time = Column(String, nullable=True)
    version_number = Column(Integer, default=1)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="variants")
    segment = relationship("Segment", back_populates="variants")
    metrics = relationship("PerformanceMetric", back_populates="variant", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Variant(id={self.id}, subject={self.subject[:30]}...)>"


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=False)
    open_rate = Column(Float, nullable=True)
    click_rate = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    variant = relationship("Variant", back_populates="metrics")
    
    def __repr__(self):
        return f"<PerformanceMetric(id={self.id}, open_rate={self.open_rate}, click_rate={self.click_rate})>"


class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    agent_name = Column(String, nullable=False)  # parser, planner, content, analytics, optimizer
    decision = Column(String, nullable=False)  # What decision was made
    reasoning = Column(Text, nullable=False)  # Why the decision was made
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(Text, nullable=True)  # JSON string for additional data
    
    def __repr__(self):
        return f"<AgentLog(id={self.id}, agent={self.agent_name}, decision={self.decision})>"
