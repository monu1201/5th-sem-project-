"""
Result Aggregator & Quality Scorer.
Merges static analysis findings with AI review results and ML defect predictions.
"""

from typing import Dict, Any, List

SEVERITY_WEIGHTS = {
    "Critical": 45,
    "High": 20,
    "Medium": 10,
    "Low": 3
}

def deduplicate_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate issues sharing matching line numbers and titles."""
    seen = set()
    deduped = []
    for issue in issues:
        key = (
            issue.get("line_number") or issue.get("line"),
            issue.get("title", "").strip().lower()[:30]
        )
        if key not in seen:
            seen.add(key)
            # Normalize field name to 'line_number'
            if "line" in issue and "line_number" not in issue:
                issue["line_number"] = issue.pop("line")
            # Normalize section-wise fields
            if not issue.get("software_defect") and issue.get("why_it_matters"):
                issue["software_defect"] = issue["why_it_matters"]
            if not issue.get("why_it_matters") and issue.get("software_defect"):
                issue["why_it_matters"] = issue["software_defect"]
            if not issue.get("bug_fix") and issue.get("recommendation"):
                issue["bug_fix"] = issue["recommendation"]
            if not issue.get("recommendation") and issue.get("bug_fix"):
                issue["recommendation"] = issue["bug_fix"]
            deduped.append(issue)
    return deduped

def calculate_quality_score(issues: List[Dict[str, Any]]) -> float:
    """Calculate 0-100 quality score penalizing for defect severity."""
    score = 100.0
    for issue in issues:
        sev = issue.get("severity", "Low")
        score -= SEVERITY_WEIGHTS.get(sev, 3)
    return max(5.0, min(100.0, round(score, 1)))

def aggregate_analysis_results(
    static_issues: List[Dict[str, Any]],
    ai_review: Dict[str, Any],
    ml_prediction: Dict[str, Any],
    metrics: Dict[str, Any],
    filename: str = "",
    language: str = "python",
    source_code: str = ""
) -> Dict[str, Any]:
    """
    Produce the final unified assessment containing quality score,
    defect prediction, classified issues, recommendations, and suggested fix code.
    """
    combined_issues = deduplicate_issues(static_issues + ai_review.get("issues", []))

    # Calculate severity counts
    critical_count = sum(1 for i in combined_issues if i.get("severity") == "Critical")
    high_count = sum(1 for i in combined_issues if i.get("severity") == "High")
    medium_count = sum(1 for i in combined_issues if i.get("severity") == "Medium")
    low_count = sum(1 for i in combined_issues if i.get("severity") == "Low")

    # Final quality score
    quality_score = calculate_quality_score(combined_issues)

    # ML defect probability
    defect_prob = ml_prediction.get("defect_probability", 0.0)
    ml_risk_level = ml_prediction.get("risk_level", "Low")

    # Joint Risk Level: Elevated if critical issues exist or defect prob is high
    if critical_count > 0 or defect_prob > 60.0 or quality_score < 60:
        joint_risk_level = "High"
    elif high_count > 0 or defect_prob > 30.0 or quality_score < 80:
        joint_risk_level = "Medium"
    else:
        joint_risk_level = "Low"

    # Build recommendations list
    recommendations = ai_review.get("recommendations", [])
    if not recommendations:
        if joint_risk_level == "High":
            recommendations.append({
                "category": "Defect Mitigation",
                "priority": "Critical",
                "title": "Immediate Refactoring Required",
                "action_plan": "Resolve detected Critical security flaws and reduce cyclomatic complexity before merging to production."
            })
        recommendations.append({
            "category": "Code Quality",
            "priority": "Medium",
            "title": "Establish CI Automated Linting",
            "action_plan": "Integrate static analysis tooling into GitHub Actions / GitLab CI to prevent security regressions."
        })

    suggested_code = ai_review.get("suggested_code") or source_code
    summary = ai_review.get("review_summary") or (
        f"Analyzed {language.upper()} code for '{filename or 'module'}'. "
        f"Detected {len(combined_issues)} issue(s). Quality score: {quality_score}/100 with {joint_risk_level} defect risk."
    )

    return {
        "filename": filename or "untitled",
        "language": language,
        "quality_score": quality_score,
        "risk_level": joint_risk_level,
        "defect_probability": defect_prob,
        "is_defect_prone": ml_prediction.get("is_defect_prone", False),
        "total_issues": len(combined_issues),
        "critical_issues": critical_count,
        "high_issues": high_count,
        "medium_issues": medium_count,
        "low_issues": low_count,
        "review_summary": summary,
        "issues": combined_issues,
        "recommendations": recommendations,
        "suggested_code": suggested_code,
        "metrics": metrics,
        "defect_prediction": ml_prediction,
        "ai_model_used": ai_review.get("provider_used", "Rule-Based Review Engine")
    }
