"""
Model evaluation module.
Generates classification reports, confusion matrix, and ROC-AUC scores.
"""

import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from ml.preprocessing import prepare_dataset, SCALER_PATH
from ml.feature_extraction import FEATURE_NAMES

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "defect_model.joblib")
CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "defect_benchmark_dataset.csv")

def evaluate_defect_model():
    if not os.path.exists(MODEL_PATH):
        from ml.train import train_defect_model
        train_defect_model()

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = pd.read_csv(CSV_PATH)
    X = df[FEATURE_NAMES]
    y = df["defective"].values

    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    y_prob = model.predict_proba(X_scaled)[:, 1]

    report = classification_report(y, y_pred, target_names=["Non-Defective", "Defect-Prone"])
    cm = confusion_matrix(y, y_pred).tolist()
    auc = roc_auc_score(y, y_prob)

    print("=== Software Defect Prediction Model Evaluation ===")
    print(report)
    print(f"ROC-AUC: {auc:.4f}")
    print(f"Confusion Matrix: {cm}")

    return {
        "classification_report": report,
        "confusion_matrix": cm,
        "roc_auc": round(float(auc), 4)
    }

if __name__ == "__main__":
    evaluate_defect_model()
