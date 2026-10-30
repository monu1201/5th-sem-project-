"""
FastAPI REST API routes for Code Review and Defect Prediction System.
"""

import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database.session import get_db, ACTIVE_DB_TYPE
from backend.app.models.entities import CodeReview, Issue, DefectPrediction, Recommendation
from backend.app.schemas.schemas import (
    AnalyzeRequest,
    PredictRequest,
    ReviewOnlyRequest,
    CodeReviewResponse,
    ReviewListItem,
    DashboardStatsResponse,
    HealthResponse
)
from backend.app.services.preprocessor import preprocess_code
from backend.app.services.static_analyzer import run_static_analysis
from backend.app.services.aggregator import aggregate_analysis_results
from backend.app.services.report_generator import generate_markdown_report, generate_html_report
from ai_engine.reviewer import perform_ai_review
from ml.predict import predict_defect_risk

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health-check endpoint detailing database and engine readiness."""
    model_loaded = os.path.exists(os.path.join(os.path.dirname(__file__), "..", "..", "ml", "models", "defect_model.joblib"))
    return {
        "status": "healthy",
        "database": "connected",
        "active_db": ACTIVE_DB_TYPE,
        "ml_model": "loaded" if model_loaded else "standby",
        "default_ai_provider": os.getenv("AI_PROVIDER", "openai/chat-gpt")
    }

@router.post("/analyze", response_model=CodeReviewResponse, status_code=status.HTTP_201_CREATED)
def analyze_code_submission(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    End-to-End Pipeline:
    1. Preprocess & Validate Code
    2. Static Code Analysis (AST & Security Patterns)
    3. AI Code Review (Gemini/OpenAI/Anthropic/Rule-Based Engine)
    4. ML Defect Prediction (Random Forest Model)
    5. Result Aggregation & Quality Scoring
    6. Persist to Database
    """
    try:
        clean_code, lang, metrics = preprocess_code(
            code=payload.code,
            filename=payload.filename or "sample.py",
            language=payload.language or "python"
        )
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))

    # 1. Static Analysis
    static_issues = run_static_analysis(clean_code, lang)

    # 2. ML Defect Prediction
    ml_res = predict_defect_risk(clean_code, lang, metrics)

    # 3. AI Code Review
    ai_res = perform_ai_review(
        code=clean_code,
        language=lang,
        static_issues=static_issues,
        metrics=metrics,
        provider_name=payload.provider,
        api_key=payload.api_key
    )

    # 4. Result Aggregation
    aggregated = aggregate_analysis_results(
        static_issues=static_issues,
        ai_review=ai_res,
        ml_prediction=ml_res,
        metrics=metrics,
        filename=payload.filename or "module",
        language=lang,
        source_code=clean_code
    )

    # 5. Persist to Database
    db_review = CodeReview(
        filename=aggregated["filename"],
        language=aggregated["language"],
        source_code=clean_code,
        quality_score=aggregated["quality_score"],
        risk_level=aggregated["risk_level"],
        defect_probability=aggregated["defect_probability"],
        total_issues=aggregated["total_issues"],
        critical_issues=aggregated["critical_issues"],
        high_issues=aggregated["high_issues"],
        medium_issues=aggregated["medium_issues"],
        low_issues=aggregated["low_issues"],
        review_summary=aggregated["review_summary"],
        suggested_code=aggregated["suggested_code"],
        ai_model_used=aggregated["ai_model_used"]
    )
    db.add(db_review)
    db.flush()

    # Add issues
    for iss in aggregated["issues"]:
        line_no = iss.get("line_number") if iss.get("line_number") is not None else iss.get("line")
        db_issue = Issue(
            review_id=db_review.id,
            issue_type=iss.get("type", "General"),
            severity=iss.get("severity", "Medium"),
            line_number=line_no,
            title=iss.get("title", "Issue"),
            description=iss.get("description", ""),
            why_it_matters=iss.get("why_it_matters", ""),
            recommendation=iss.get("recommendation", ""),
            suggested_fix=iss.get("suggested_fix", ""),
            software_defect=iss.get("software_defect") or iss.get("why_it_matters", ""),
            bug_fix=iss.get("bug_fix") or iss.get("recommendation", ""),
            future_guidelines=iss.get("future_guidelines", "")
        )
        db.add(db_issue)

    # Add ML prediction
    db_prediction = DefectPrediction(
        review_id=db_review.id,
        defect_probability=ml_res["defect_probability"],
        risk_level=ml_res["risk_level"],
        is_defect_prone=ml_res["is_defect_prone"],
        model_name=ml_res["model_name"],
        cyclomatic_complexity=metrics.get("cyclomatic_complexity", 1.0),
        loc=metrics.get("loc", 0),
        nesting_depth=metrics.get("max_nesting_depth", 0),
        function_count=metrics.get("num_functions", 0),
        class_count=metrics.get("num_classes", 0),
        smell_count=metrics.get("code_smell_indicators", 0),
        feature_vector_json=metrics,
        top_risk_factors_json=ml_res.get("top_risk_factors", [])
    )
    db.add(db_prediction)

    # Add recommendations
    for rec in aggregated["recommendations"]:
        db_rec = Recommendation(
            review_id=db_review.id,
            category=rec.get("category", "General"),
            priority=rec.get("priority", "Medium"),
            title=rec.get("title", "Recommendation"),
            action_plan=rec.get("action_plan", "")
        )
        db.add(db_rec)

    db.commit()
    db.refresh(db_review)

    # Convert to response
    return _build_review_response(db_review)

@router.post("/review")
def review_only(payload: ReviewOnlyRequest):
    """Run AI code review directly without persistence."""
    try:
        clean_code, lang, metrics = preprocess_code(payload.code, language=payload.language or "python")
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    static_issues = run_static_analysis(clean_code, lang)
    return perform_ai_review(
        code=clean_code,
        language=lang,
        static_issues=static_issues,
        metrics=metrics,
        provider_name=payload.provider,
        api_key=payload.api_key
    )

@router.post("/predict")
def predict_only(payload: PredictRequest):
    """Run ML defect probability prediction directly."""
    try:
        clean_code, lang, metrics = preprocess_code(payload.code, language=payload.language or "python")
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    
    return predict_defect_risk(clean_code, lang, metrics)

@router.get("/reviews", response_model=List[ReviewListItem])
def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    risk_level: Optional[str] = None,
    language: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Fetch previous code reviews with filtering and pagination."""
    query = db.query(CodeReview)
    if risk_level:
        query = query.filter(CodeReview.risk_level == risk_level)
    if language:
        query = query.filter(CodeReview.language == language.lower())
    if search:
        query = query.filter(CodeReview.filename.ilike(f"%{search}%"))

    reviews = query.order_by(desc(CodeReview.created_at)).offset(skip).limit(limit).all()
    return reviews

@router.get("/reviews/{review_id}", response_model=CodeReviewResponse)
def get_review_detail(review_id: str, db: Session = Depends(get_db)):
    """Fetch complete review details including issues, prediction, and recommendations."""
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return _build_review_response(review)

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: str, db: Session = Depends(get_db)):
    """Delete a code review record."""
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/reviews/{review_id}/report")
def export_review_report(
    review_id: str,
    format: str = Query("markdown", pattern="^(markdown|json|html)$"),
    db: Session = Depends(get_db)
):
    """Download analysis report in Markdown, JSON, or printable HTML."""
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    resp_dict = _build_review_response(review).model_dump()

    if format == "json":
        return resp_dict
    elif format == "html":
        html_content = generate_html_report(resp_dict)
        return Response(content=html_content, media_type="text/html")
    else: # markdown
        md_content = generate_markdown_report(resp_dict)
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename=review_{review_id}.md"}
        )

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_statistics(db: Session = Depends(get_db)):
    """Aggregate KPI statistics and distributions for dashboard visualization."""
    total_reviews = db.query(CodeReview).count()
    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "total_issues": 0,
            "critical_issues": 0,
            "high_risk_files": 0,
            "avg_quality_score": 100.0,
            "avg_defect_probability": 0.0,
            "severity_distribution": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0},
            "risk_distribution": {"Low": 0, "Medium": 0, "High": 0},
            "quality_trend": [],
            "recent_reviews": []
        }

    reviews = db.query(CodeReview).order_by(desc(CodeReview.created_at)).all()
    
    total_issues = sum(r.total_issues for r in reviews)
    critical_issues = sum(r.critical_issues for r in reviews)
    high_risk_files = sum(1 for r in reviews if r.risk_level == "High")
    avg_quality = round(sum(r.quality_score for r in reviews) / total_reviews, 1)
    avg_defect_prob = round(sum(r.defect_probability for r in reviews) / total_reviews, 1)

    # Severity distribution
    sev_dist = {
        "Critical": critical_issues,
        "High": sum(r.high_issues for r in reviews),
        "Medium": sum(r.medium_issues for r in reviews),
        "Low": sum(r.low_issues for r in reviews)
    }

    # Risk distribution
    risk_dist = {
        "Low": sum(1 for r in reviews if r.risk_level == "Low"),
        "Medium": sum(1 for r in reviews if r.risk_level == "Medium"),
        "High": high_risk_files
    }

    # Trend (last 10 reviews in chronological order)
    trend_reviews = list(reversed(reviews[:10]))
    quality_trend = [
        {
            "index": i + 1,
            "name": r.filename[:12],
            "quality": r.quality_score,
            "defect_probability": r.defect_probability,
            "date": r.created_at.strftime("%b %d")
        }
        for i, r in enumerate(trend_reviews)
    ]

    recent_reviews = reviews[:6]

    return {
        "total_reviews": total_reviews,
        "total_issues": total_issues,
        "critical_issues": critical_issues,
        "high_risk_files": high_risk_files,
        "avg_quality_score": avg_quality,
        "avg_defect_probability": avg_defect_prob,
        "severity_distribution": sev_dist,
        "risk_distribution": risk_dist,
        "quality_trend": quality_trend,
        "recent_reviews": recent_reviews
    }

@router.get("/samples")
def get_sample_codes():
    """Return pre-built code samples showcasing intentional bugs and security vulnerabilities."""
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "samples")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "samples")),
        os.path.abspath("samples")
    ]
    samples_dir = next((p for p in candidates if os.path.exists(p)), candidates[0])
    samples = []
    
    if os.path.exists(samples_dir):
        for f in sorted(os.listdir(samples_dir)):
            file_path = os.path.join(samples_dir, f)
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as sfile:
                    content = sfile.read()
                lang = "python"
                if f.endswith(".js"): lang = "javascript"
                elif f.endswith(".java"): lang = "java"
                elif f.endswith(".cpp") or f.endswith(".c") or f.endswith(".h"): lang = "cpp"
                samples.append({
                    "filename": f,
                    "language": lang,
                    "code": content,
                    "label": f.replace("sample_", "").replace(".py", "").replace(".js", "").replace(".java", "").replace(".cpp", "").replace("_", " ").title()
                })
    return samples

def _build_review_response(review: CodeReview) -> CodeReviewResponse:
    prediction = None
    if review.defect_prediction:
        dp = review.defect_prediction
        prediction = {
            "defect_probability": dp.defect_probability,
            "risk_level": dp.risk_level,
            "is_defect_prone": dp.is_defect_prone,
            "model_name": dp.model_name,
            "model_notice": "Trained with NASA/PROMISE defect distributions. Swap with enterprise telemetry when deployed.",
            "top_risk_factors": dp.top_risk_factors_json or []
        }

    metrics = {}
    if review.defect_prediction and review.defect_prediction.feature_vector_json:
        metrics = review.defect_prediction.feature_vector_json

    return CodeReviewResponse(
        id=review.id,
        filename=review.filename,
        language=review.language,
        quality_score=review.quality_score,
        risk_level=review.risk_level,
        defect_probability=review.defect_probability,
        total_issues=review.total_issues,
        critical_issues=review.critical_issues,
        high_issues=review.high_issues,
        medium_issues=review.medium_issues,
        low_issues=review.low_issues,
        review_summary=review.review_summary,
        source_code=review.source_code,
        suggested_code=review.suggested_code,
        ai_model_used=review.ai_model_used,
        created_at=review.created_at,
        issues=[
            {
                "id": i.id,
                "type": i.issue_type,
                "severity": i.severity,
                "line_number": i.line_number,
                "title": i.title,
                "description": i.description,
                "why_it_matters": i.why_it_matters,
                "recommendation": i.recommendation,
                "suggested_fix": i.suggested_fix,
                "software_defect": getattr(i, "software_defect", None) or i.why_it_matters,
                "bug_fix": getattr(i, "bug_fix", None) or i.recommendation,
                "future_guidelines": getattr(i, "future_guidelines", None)
            }
            for i in review.issues
        ],
        recommendations=[
            {
                "id": r.id,
                "category": r.category,
                "priority": r.priority,
                "title": r.title,
                "action_plan": r.action_plan
            }
            for r in review.recommendations
        ],
        metrics=metrics,
        defect_prediction=prediction
    )
