"""
Preprocessing and transformation pipeline for defect prediction.
Handles feature scaling, vectorization, and dataset loading.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, List, Optional
from ml.feature_extraction import FEATURE_NAMES

SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "metrics_scaler.joblib")

def get_or_fit_scaler(X: Optional[pd.DataFrame] = None) -> StandardScaler:
    """Load existing scaler or fit a new one on provided features."""
    if os.path.exists(SCALER_PATH) and X is None:
        return joblib.load(SCALER_PATH)
    
    scaler = StandardScaler()
    if X is not None:
        scaler.fit(X[FEATURE_NAMES])
        os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
        joblib.dump(scaler, SCALER_PATH)
    return scaler

def prepare_dataset(csv_path: str) -> Tuple[np.ndarray, np.ndarray, StandardScaler]:
    """Load dataset, extract features and target, and apply scaling."""
    df = pd.read_csv(csv_path)
    X = df[FEATURE_NAMES]
    y = df["defective"].values
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    
    return X_scaled, y, scaler

def scale_features(feature_vector: List[float], scaler: Optional[StandardScaler] = None) -> np.ndarray:
    """Scale a single raw feature vector for model inference."""
    if scaler is None:
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
        else:
            return np.array([feature_vector])
    df_feat = pd.DataFrame([feature_vector], columns=FEATURE_NAMES)
    return scaler.transform(df_feat)
