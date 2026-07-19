# src/models.py
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from src.database import Base

class Student(Base):
    __tablename__ = "students"

    student_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    parent_phone = Column(String, nullable=True)     # Target for WhatsApp
    parent_email = Column(String, nullable=True)     # Target for email escalations
    mentor_email = Column(String, nullable=True)     # Secondary instructor tier
    current_cgpa = Column(Float, default=4.0)

    # Clean multi-table relationships
    metrics = relationship("AcademicMetric", back_populates="student", cascade="all, delete-orphan")
    escalations = relationship("EscalationLog", back_populates="student", cascade="all, delete-orphan")

class AcademicMetric(Base):
    __tablename__ = "academic_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    attendance_percentage = Column(Float, nullable=False)
    assignment_score = Column(Float, nullable=True)  # Scored out of 100
    exam_score = Column(Float, nullable=True)        # Scored out of 100
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="metrics")

class EscalationLog(Base):
    __tablename__ = "escalation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    risk_level = Column(String, nullable=False)      # "Low", "Medium", "Critical"
    urgency_score = Column(Float, nullable=False)
    action_summary = Column(String, nullable=True)
    is_active = Column(Integer, default=1)           # 1 = Active alert loop, 0 = De-escalated (Recovered)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="escalations")

class SyllabusLog(Base):
    __tablename__ = 'syllabus_log'
    
    id = Column(Integer, primary_key=True, index=True)
    topic_covered = Column(String, nullable=False)
    resource_link = Column(String, nullable=False)
    lab_assignment = Column(String, nullable=False)