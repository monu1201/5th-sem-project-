"""
Synthetic / Benchmark dataset generator for Software Defect Prediction.
Models software metrics distribution based on NASA MDP (KC1, JM1) and PROMISE repository patterns.
This provides a clean, reproducible development baseline that can be swapped with real-world CSVs.
"""

import os
import numpy as np
import pandas as pd
from ml.feature_extraction import FEATURE_NAMES

def generate_defect_dataset(num_samples: int = 1500, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)
    
    # Generate realistic software module metrics
    loc = np.random.exponential(scale=70, size=num_samples).astype(int) + 10
    sloc = (loc * np.random.uniform(0.65, 0.85, size=num_samples)).astype(int)
    comment_lines = (loc * np.random.uniform(0.05, 0.20, size=num_samples)).astype(int)
    blank_lines = loc - sloc - comment_lines
    blank_lines = np.maximum(blank_lines, 0)
    
    # Cyclomatic complexity correlates strongly with SLOC + stochastic variance
    base_cc = 1 + (sloc / np.random.uniform(8, 16, size=num_samples))
    cyclomatic_complexity = np.maximum(1, np.round(base_cc + np.random.normal(0, 1.5, size=num_samples), 1))
    
    # Nesting depth: log-normal skew
    max_nesting_depth = np.random.choice([1, 2, 3, 4, 5, 6, 7], size=num_samples, p=[0.25, 0.35, 0.20, 0.10, 0.05, 0.03, 0.02])
    
    num_functions = np.maximum(1, np.round(sloc / np.random.uniform(15, 35, size=num_samples)).astype(int))
    num_classes = np.random.choice([0, 1, 2, 3, 4], size=num_samples, p=[0.40, 0.40, 0.12, 0.05, 0.03])
    avg_func_loc = np.round(sloc / num_functions, 2)
    
    # Halstead volume & difficulty
    halstead_volume = np.round(sloc * np.random.uniform(40, 90, size=num_samples), 2)
    halstead_difficulty = np.round(cyclomatic_complexity * np.random.uniform(1.5, 4.0, size=num_samples), 2)
    
    # Smells and security indicators
    code_smell_indicators = np.maximum(0, (max_nesting_depth >= 4).astype(int) * 2 + (cyclomatic_complexity > 10).astype(int) * 3 + np.random.poisson(0.5, size=num_samples))
    security_risk_indicators = np.random.choice([0, 1, 2, 3], size=num_samples, p=[0.75, 0.18, 0.05, 0.02])

    # Defect probability formula (logistic function of risk metrics)
    z = (
        -3.2 
        + 0.012 * loc 
        + 0.15 * cyclomatic_complexity 
        + 0.45 * max_nesting_depth 
        + 0.35 * code_smell_indicators 
        + 0.85 * security_risk_indicators 
        - 0.05 * (comment_lines / np.maximum(loc, 1) * 100) # comments reduce defects
        + np.random.normal(0, 0.5, size=num_samples)
    )
    
    true_prob = 1.0 / (1.0 + np.exp(-z))
    # Binary defect classification (0 = clean, 1 = defect-prone)
    is_defective = (true_prob >= 0.45).astype(int)

    df = pd.DataFrame({
        "loc": loc,
        "sloc": sloc,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "cyclomatic_complexity": cyclomatic_complexity,
        "max_nesting_depth": max_nesting_depth,
        "num_functions": num_functions,
        "num_classes": num_classes,
        "avg_func_loc": avg_func_loc,
        "halstead_volume": halstead_volume,
        "halstead_difficulty": halstead_difficulty,
        "code_smell_indicators": code_smell_indicators,
        "security_risk_indicators": security_risk_indicators,
        "defect_probability_ground_truth": np.round(true_prob, 3),
        "defective": is_defective
    })

    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__))
    os.makedirs(out_dir, exist_ok=True)
    df = generate_defect_dataset()
    csv_path = os.path.join(out_dir, "defect_benchmark_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated benchmark dataset with {len(df)} records at: {csv_path}")
    print(f"Defect rate: {df['defective'].mean():.2%}")
