"""
evaluate.py
-----------
Loads the metrics.json produced by train.py (real numbers from the actual
test-set run - never fabricated) so other parts of the app (the
GET /api/model/metrics endpoint, the AI Technology page) can read them
without needing TensorFlow loaded or retraining anything.
"""
import json
import os

from app.ml.preprocess import MODELS_DIR

METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")
FEATURE_CONFIG_PATH = os.path.join(MODELS_DIR, "feature_config.json")


def get_metrics() -> dict:
    if not os.path.exists(METRICS_PATH):
        raise FileNotFoundError(
            "No trained model metrics found. Run `python -m app.ml.train` first."
        )
    with open(METRICS_PATH) as f:
        return json.load(f)


def get_feature_config() -> dict:
    if not os.path.exists(FEATURE_CONFIG_PATH):
        raise FileNotFoundError(
            "No feature config found. Run `python -m app.ml.train` first."
        )
    with open(FEATURE_CONFIG_PATH) as f:
        return json.load(f)


if __name__ == "__main__":
    print(json.dumps(get_metrics(), indent=2))
