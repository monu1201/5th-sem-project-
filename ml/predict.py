"""
Inference module for Software Defect Prediction.
Predicts defect probability, risk level, defect prone classification, and top risk factors.
"""

import os
import joblib
import numpy as np
from typing import Dict, Any, List
from ml.feature_extraction import extract_code_metrics, metrics_to_feature_vector, FEATURE_NAMES
from ml.preprocessing import scale_features
from ml.model import calculate_risk_level

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "defect_model.joblib")

_CACHED_MODEL = None

def get_loaded_model():
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL
    
    if not os.path.exists(MODEL_PATH):
        # Auto-train if model artifact is missing
        from ml.train import train_defect_model
        train_defect_model()
    
    _CACHED_MODEL = joblib.load(MODEL_PATH)
    return _CACHED_MODEL

def identify_top_risk_factors(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Determine which specific metrics are elevating defect risk."""
    factors = []
    cc = metrics.get("cyclomatic_complexity", 1.0)
    if cc > 10.0:
        factors.append({
            "factor": "Cyclomatic Complexity",
            "value": cc,
            "threshold": 10.0,
            "impact": "High",
            "message": f"Cyclomatic complexity ({cc}) indicates excessively branched control flow."
        })
    elif cc > 6.0:
        factors.append({
            "factor": "Cyclomatic Complexity",
            "value": cc,
            "threshold": 6.0,
            "impact": "Moderate",
            "message": f"Cyclomatic complexity ({cc}) is moderate; consider refactoring nested conditionals."
        })

    nesting = metrics.get("max_nesting_depth", 0)
    if nesting >= 4:
        factors.append({
            "factor": "Deep Nesting Depth",
            "value": nesting,
            "threshold": 4,
            "impact": "High",
            "message": f"Nesting depth ({nesting}) exceeds recommended limit of 3 levels."
        })

    loc = metrics.get("loc", 0)
    if loc > 250:
        factors.append({
            "factor": "Large Module Size",
            "value": loc,
            "threshold": 200,
            "impact": "Moderate",
            "message": f"Module length ({loc} LOC) increases maintenance overhead and bug probability."
        })

    smells = metrics.get("code_smell_indicators", 0)
    if smells > 2:
        factors.append({
            "factor": "Code Smell Density",
            "value": smells,
            "threshold": 2,
            "impact": "High",
            "message": f"{smells} architectural smell indicators detected."
        })

    sec = metrics.get("security_risk_indicators", 0)
    if sec > 0:
        factors.append({
            "factor": "Security Insecurities",
            "value": sec,
            "threshold": 0,
            "impact": "Critical",
            "message": f"{sec} security vulnerability patterns found in source code."
        })

    return factors

def predict_defect_risk(code: str, language: str = "python", metrics: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main prediction entrypoint.
    Returns defect probability (0-100), risk level (Low, Medium, High),
    defect proneness, top risk factors, and development dataset disclaimer.
    """
    if metrics is None:
        metrics = extract_code_metrics(code, language)

    vector = metrics_to_feature_vector(metrics)
    model = get_loaded_model()
    
    # Scale feature vector
    X_scaled = scale_features(vector)
    
    prob_array = model.predict_proba(X_scaled)[0]
    defect_probability = float(prob_array[1]) * 100.0
    defect_probability = round(defect_probability, 1)

    risk_level = calculate_risk_level(defect_probability)
    is_defect_prone = defect_probability >= 45.0
    top_factors = identify_top_risk_factors(metrics)

    return {
        "defect_probability": defect_probability,
        "risk_level": risk_level,
        "is_defect_prone": is_defect_prone,
        "model_name": "Random Forest Classifier (NASA/PROMISE Distribution Baseline)",
        "model_notice": "Development/Demo Prediction: Trained on synthetic NASA/PROMISE defect distributions. Can be swapped with proprietary defect telemetry.",
        "metrics": metrics,
        "top_risk_factors": top_factors
    }

if __name__ == "__main__":
    sample_code = """
def process_user_data(query, db):
    # intentional complexity and raw sql
    if query:
        if len(query) > 5:
            for item in query:
                if item == 'admin':
                    db.execute("SELECT * FROM users WHERE role = '" + item + "'")
                elif item == 'guest':
                    for sub in range(10):
                        if sub > 5:
                            print(sub)
    """
    res = predict_defect_risk(sample_code, "python")
    print("Prediction Result:")
    print(f"Defect Probability: {res['defect_probability']}%")
    print(f"Risk Level: {res['risk_level']}")
    print(f"Is Defect Prone: {res['is_defect_prone']}")
    print(f"Risk Factors: {len(res['top_risk_factors'])}")
