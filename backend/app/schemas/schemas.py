"""
Pydantic v2 schemas for API validation and serialization.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AnalyzeRequest(BaseModel):
    code: str = Field(..., description="Source code text to analyze")
    filename: Optional[str] = Field("sample.py", description="Source code filename")
    language: Optional[str] = Field("python", description="Programming language: python, javascript, java, cpp")
    project_name: Optional[str] = Field("Default Project", description="Target project container")
    provider: Optional[str] = Field(None, description="AI Provider: gemini, openai, anthropic, ollama, or none")
    api_key: Optional[str] = Field(None, description="Optional per-request AI API key")

class PredictRequest(BaseModel):
    code: str = Field(..., description="Source code text for ML defect scoring")
    language: Optional[str] = Field("python", description="Language of source code")

class ReviewOnlyRequest(BaseModel):
    code: str = Field(..., description="Source code text")
    language: Optional[str] = Field("python", description="Language")
    provider: Optional[str] = None
    api_key: Optional[str] = None

class IssueSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = None
    issue_type: str = Field(..., alias="type")
    severity: str
    line_number: Optional[int] = None
    title: str
    description: str
    why_it_matters: Optional[str] = None
    recommendation: Optional[str] = None
    suggested_fix: Optional[str] = None
    software_defect: Optional[str] = None
    bug_fix: Optional[str] = None
    future_guidelines: Optional[str] = None

class RecommendationSchema(BaseModel):
    id: Optional[str] = None
    category: str
    priority: str
    title: str
    action_plan: str

class DefectPredictionSchema(BaseModel):
    defect_probability: float
    risk_level: str
    is_defect_prone: bool
    model_name: str
    model_notice: Optional[str] = None
    top_risk_factors: List[Dict[str, Any]] = []

class CodeReviewResponse(BaseModel):
    id: str
    filename: str
    language: str
    quality_score: float
    risk_level: str
    defect_probability: float
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    review_summary: Optional[str] = None
    source_code: str
    suggested_code: Optional[str] = None
    ai_model_used: str
    created_at: datetime
    issues: List[IssueSchema] = []
    recommendations: List[RecommendationSchema] = []
    metrics: Dict[str, Any] = {}
    defect_prediction: Optional[DefectPredictionSchema] = None

class ReviewListItem(BaseModel):
    id: str
    filename: str
    language: str
    quality_score: float
    risk_level: str
    defect_probability: float
    total_issues: int
    critical_issues: int
    created_at: datetime

class DashboardStatsResponse(BaseModel):
    total_reviews: int
    total_issues: int
    critical_issues: int
    high_risk_files: int
    avg_quality_score: float
    avg_defect_probability: float
    severity_distribution: Dict[str, int]
    risk_distribution: Dict[str, int]
    quality_trend: List[Dict[str, Any]]
    recent_reviews: List[ReviewListItem]

class HealthResponse(BaseModel):
    status: str
    database: str
    active_db: str
    ml_model: str
    default_ai_provider: str
