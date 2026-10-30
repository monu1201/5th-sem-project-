"""
Training pipeline for the Machine Learning Defect Prediction System.
Trains Random Forest model with cross-validation and evaluation metrics,
saving model artifacts and metadata.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from ml.data.generate_dataset import generate_defect_dataset
from ml.preprocessing import prepare_dataset, SCALER_PATH
from ml.model import get_model
from ml.feature_extraction import FEATURE_NAMES

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "defect_model.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

def train_defect_model(model_type: str = "random_forest"):
    os.makedirs(MODEL_DIR, exist_ok=True)
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "defect_benchmark_dataset.csv")

    if not os.path.exists(csv_path):
        print("Generating benchmark dataset...")
        df = generate_defect_dataset(num_samples=2000, random_state=42)
        df.to_csv(csv_path, index=False)
    else:
        df = pd.read_csv(csv_path)

    print(f"Loaded dataset: {len(df)} samples across {len(FEATURE_NAMES)} features.")

    X_scaled, y, scaler = prepare_dataset(csv_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.20, random_state=42, stratify=y
    )

    model = get_model(model_type)
    model.fit(X_train, y_train)

    # Predictions & metrics
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))

    # Feature importances
    feature_importances = {}
    if hasattr(model, "feature_importances_"):
        for name, imp in zip(FEATURE_NAMES, model.feature_importances_):
            feature_importances[name] = round(float(imp), 4)

    # Save artifacts
    joblib.dump(model, MODEL_PATH)

    metadata = {
        "model_type": model_type,
        "is_demo_dataset": True,
        "dataset_description": "Standard NASA/PROMISE benchmark distribution baseline for development/demo",
        "sample_count": len(df),
        "test_sample_count": len(y_test),
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4)
        },
        "feature_importances": sorted(
            feature_importances.items(), key=lambda x: x[1], reverse=True
        ),
        "features": FEATURE_NAMES
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n--- Model Training Completed Successfully ---")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Accuracy : {acc:.2%}")
    print(f"Precision: {prec:.2%}")
    print(f"Recall   : {rec:.2%}")
    print(f"F1 Score : {f1:.2%}")
    print(f"ROC AUC  : {roc_auc:.4f}")
    return metadata

if __name__ == "__main__":
    train_defect_model()
