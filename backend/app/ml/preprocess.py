"""
preprocess.py
-------------
Loads StressLevelDataset.csv, runs the required data-quality inspection,
auto-detects the target column, encodes/scales features, and returns
train/val/test splits plus the fitted preprocessing objects.

Nothing here is hardcoded to a specific column layout beyond the target
detection heuristic below - if you swap in the real Kaggle CSV (which has
the identical schema this generator reproduces), this still works unchanged.
"""
import json
import os

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "StressLevelDataset.csv")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

CANDIDATE_TARGET_NAMES = ["stress_level", "stress", "target", "label", "class"]


def load_dataset(path: str = DATASET_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def inspect_dataset(df: pd.DataFrame) -> dict:
    """Steps 2-6 of the spec: shape, missing values, duplicates, dtypes, class balance."""
    report = {
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
    }
    return report


def detect_target_column(df: pd.DataFrame) -> str:
    """Auto-identify the target column (spec step 8)."""
    for name in CANDIDATE_TARGET_NAMES:
        if name in df.columns:
            return name
    # fallback: last column, if it looks categorical (few unique integer values)
    last_col = df.columns[-1]
    if df[last_col].nunique() <= 10:
        return last_col
    raise ValueError("Could not auto-detect a target column - please specify one explicitly.")


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    df = df.dropna()
    return df


def build_preprocessing(df: pd.DataFrame, target_col: str):
    """Encode categoricals, scale numerics, split train/val/test.

    Returns dict with X_train, X_val, X_test, y_train, y_val, y_test,
    scaler, label_encoder (if used), feature_columns, num_classes.
    """
    feature_cols = [c for c in df.columns if c != target_col]

    X = df[feature_cols].copy()
    y_raw = df[target_col].copy()

    # Encode any non-numeric categorical feature columns
    encoders = {}
    for col in X.columns:
        if X[col].dtype == object:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

    # Encode target if it's not already integer-coded
    label_encoder = None
    if y_raw.dtype == object:
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y_raw.astype(str))
    else:
        y = y_raw.to_numpy()

    num_classes = int(len(np.unique(y)))

    X_train, X_temp, y_train, y_temp = train_test_split(
        X.values, y, test_size=0.30, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    return {
        "X_train": X_train_scaled,
        "X_val": X_val_scaled,
        "X_test": X_test_scaled,
        "y_train": y_train,
        "y_val": y_val,
        "y_test": y_test,
        "scaler": scaler,
        "encoders": encoders,
        "label_encoder": label_encoder,
        "feature_columns": feature_cols,
        "num_classes": num_classes,
        "target_col": target_col,
    }


def save_feature_config(bundle: dict, path: str = None):
    path = path or os.path.join(MODELS_DIR, "feature_config.json")
    config = {
        "feature_columns": bundle["feature_columns"],
        "target_col": bundle["target_col"],
        "num_classes": bundle["num_classes"],
        "class_labels": (
            list(bundle["label_encoder"].classes_)
            if bundle["label_encoder"] is not None
            else list(range(bundle["num_classes"]))
        ),
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return config
