"""
Defect Prediction model wrappers and risk categorization utilities.
"""

from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

def get_model(model_type: str = "random_forest"):
    """Instantiate classification model with tuned hyperparameters."""
    if model_type == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    else:
        return RandomForestClassifier(
            n_estimators=120,
            max_depth=8,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced"
        )

def calculate_risk_level(defect_probability_pct: float) -> str:
    """
    Standard risk classification:
    0–30%   -> Low
    31–60%  -> Medium
    61–100% -> High
    """
    if defect_probability_pct <= 30.0:
        return "Low"
    elif defect_probability_pct <= 60.0:
        return "Medium"
    else:
        return "High"
