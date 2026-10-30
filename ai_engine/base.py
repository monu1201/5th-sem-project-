"""
Base abstract class for AI Code Review providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAIReviewer(ABC):
    """Abstract base class that all AI review providers must implement."""

    def __init__(self, api_key: str = "", model_name: str = ""):
        self.api_key = api_key
        self.model_name = model_name

    @abstractmethod
    def review_code(
        self,
        code: str,
        language: str,
        static_issues: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze code and return structured review dictionary:
        {
            "quality_score": float,
            "risk_level": "Low" | "Medium" | "High",
            "review_summary": str,
            "issues": [...],
            "recommendations": [...],
            "suggested_code": str
        }
        """
        pass
