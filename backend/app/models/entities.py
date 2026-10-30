"""
SQLAlchemy ORM models representing the code review, defect prediction,
and software audit schema.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    files = relationship("File", back_populates="project", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    filename = Column(String(255), nullable=False)
    language = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    lines_of_code = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="files")
    reviews = relationship("CodeReview", back_populates="file", cascade="all, delete-orphan")

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    file_id = Column(String(36), ForeignKey("files.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String(255), nullable=False)
    language = Column(String(50), nullable=False)
    source_code = Column(Text, nullable=False)
    quality_score = Column(Float, nullable=False, default=100.0)
    risk_level = Column(String(20), nullable=False, default="Low") # Low, Medium, High
    defect_probability = Column(Float, nullable=False, default=0.0)
    total_issues = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    review_summary = Column(Text, nullable=True)
    suggested_code = Column(Text, nullable=True)
    ai_model_used = Column(String(100), default="Rule-Based Review Engine")
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("File", back_populates="reviews")
    issues = relationship("Issue", back_populates="review", cascade="all, delete-orphan")
    defect_prediction = relationship("DefectPrediction", back_populates="review", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="review", cascade="all, delete-orphan")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    review_id = Column(String(36), ForeignKey("code_reviews.id", ondelete="CASCADE"), nullable=False)
    issue_type = Column(String(50), nullable=False) # Security, Bug, Code Smell, Maintainability
    severity = Column(String(20), nullable=False)   # Critical, High, Medium, Low
    line_number = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    suggested_fix = Column(Text, nullable=True)
    software_defect = Column(Text, nullable=True)
    bug_fix = Column(Text, nullable=True)
    future_guidelines = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("CodeReview", back_populates="issues")

class DefectPrediction(Base):
    __tablename__ = "defect_predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    review_id = Column(String(36), ForeignKey("code_reviews.id", ondelete="CASCADE"), nullable=False)
    defect_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    is_defect_prone = Column(Boolean, default=False)
    model_name = Column(String(100), default="Random Forest Classifier")
    cyclomatic_complexity = Column(Float, default=0.0)
    loc = Column(Integer, default=0)
    nesting_depth = Column(Integer, default=0)
    function_count = Column(Integer, default=0)
    class_count = Column(Integer, default=0)
    smell_count = Column(Integer, default=0)
    feature_vector_json = Column(JSON, nullable=True)
    top_risk_factors_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("CodeReview", back_populates="defect_prediction")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    review_id = Column(String(36), ForeignKey("code_reviews.id", ondelete="CASCADE"), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    action_plan = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    review = relationship("CodeReview", back_populates="recommendations")
