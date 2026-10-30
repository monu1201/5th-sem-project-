"""
AI Reviewer orchestrator.
Manages provider execution with graceful error recovery and structured output validation.
"""

import logging
from typing import Dict, Any, List, Optional
from ai_engine.provider import get_ai_provider, DeterministicRuleProvider

logger = logging.getLogger("ai_reviewer")

def perform_ai_review(
    code: str,
    language: str = "python",
    static_issues: Optional[List[Dict[str, Any]]] = None,
    metrics: Optional[Dict[str, Any]] = None,
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes AI code review with fallback resilience.
    Guarantees a valid structured review dictionary even under network or quota errors.
    """
    if static_issues is None:
        static_issues = []
    if metrics is None:
        metrics = {}

    provider = get_ai_provider(provider_name, api_key, model_name)
    provider_label = type(provider).__name__.replace("Provider", "")

    try:
        review_result = provider.review_code(code, language, static_issues, metrics)
        review_result["provider_used"] = f"{provider_label} AI Engine"
        review_result["is_live_ai"] = not isinstance(provider, DeterministicRuleProvider)
        return review_result
    except Exception as exc:
        logger.warning(f"AI Provider {provider_label} encountered error: {exc}. Falling back to Rule-Based Engine.")
        fallback = DeterministicRuleProvider()
        review_result = fallback.review_code(code, language, static_issues, metrics)
        review_result["provider_used"] = "Rule-Based Review Engine (Fallback)"
        review_result["is_live_ai"] = False
        review_result["fallback_reason"] = str(exc)
        return review_result
