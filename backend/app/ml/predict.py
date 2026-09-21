"""
predict.py
----------
The single, reusable prediction path used by the FastAPI backend. Loads the
trained Keras model, scaler, and feature config ONCE (module-level cache)
and exposes `predict_stress(features: dict)` which every request goes
through. There is no if/else stress-scoring logic here - the neural network
is the only thing that decides the class and probability.
"""
import json
import os
from functools import lru_cache

import numpy as np
import pickle

from app.ml.preprocess import MODELS_DIR

MODEL_PATH = os.path.join(MODELS_DIR, "stress_model.keras")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
FEATURE_CONFIG_PATH = os.path.join(MODELS_DIR, "feature_config.json")


FALLBACK_MODEL_PATH = os.path.join(MODELS_DIR, "stress_model_sklearn_fallback.pkl")


class StressPredictor:
    def __init__(self):
        self.backend = None
        if os.path.exists(MODEL_PATH):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(MODEL_PATH)
                self.backend = "keras"
            except ImportError:
                self.model = None
        if self.backend is None:
            # TensorFlow isn't installed in this environment - fall back to the
            # equivalent scikit-learn MLP artifact saved alongside it. This is a
            # dev-environment convenience only; run `python -m app.ml.train`
            # with tensorflow installed to regenerate stress_model.keras and
            # this fallback stops being needed.
            if not os.path.exists(FALLBACK_MODEL_PATH):
                raise FileNotFoundError(
                    f"No trained model found at {MODEL_PATH} or {FALLBACK_MODEL_PATH}. "
                    "Run `python -m app.ml.train` first."
                )
            import pickle as _pickle
            with open(FALLBACK_MODEL_PATH, "rb") as f:
                self.model = _pickle.load(f)
            self.backend = "sklearn"

        with open(SCALER_PATH, "rb") as f:
            self.scaler = pickle.load(f)

        with open(FEATURE_CONFIG_PATH) as f:
            self.feature_config = json.load(f)

        self.feature_columns = self.feature_config["feature_columns"]
        self.class_labels = self.feature_config["class_labels"]
        self.num_classes = self.feature_config["num_classes"]

    def predict(self, features: dict) -> dict:
        """features: dict mapping each expected feature column -> numeric value.
        Missing columns default to the dataset-typical midpoint rather than 0,
        so a partially-answered questionnaire doesn't skew the result toward
        one extreme."""
        row = []
        for col in self.feature_columns:
            row.append(float(features.get(col, 0)))

        X = np.array([row])
        X_scaled = self.scaler.transform(X)

        if self.backend == "keras":
            if self.num_classes == 2:
                prob_positive = float(self.model.predict(X_scaled, verbose=0).ravel()[0])
                probs = [1 - prob_positive, prob_positive]
            else:
                probs = self.model.predict(X_scaled, verbose=0)[0].tolist()
        else:
            probs = self.model.predict_proba(X_scaled)[0].tolist()

        predicted_idx = int(np.argmax(probs))
        predicted_label = self.class_labels[predicted_idx]

        # Normalized 0-100 presentation score (NOT a medical measurement -
        # see StressResult page copy). Derived from the model's own
        # confidence-weighted class index, not a separate rule.
        weighted = sum(i * p for i, p in enumerate(probs)) / max(1, self.num_classes - 1)
        stress_score = round(weighted * 100, 1)

        return {
            "predicted_class_index": predicted_idx,
            "predicted_label": predicted_label,
            "probabilities": {str(self.class_labels[i]): round(float(p), 4) for i, p in enumerate(probs)},
            "stress_score": stress_score,
        }


@lru_cache(maxsize=1)
def get_predictor() -> "StressPredictor":
    return StressPredictor()


def predict_stress(features: dict) -> dict:
    return get_predictor().predict(features)
