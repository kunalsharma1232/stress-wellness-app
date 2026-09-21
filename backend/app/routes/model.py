from fastapi import APIRouter, HTTPException

from app.ml.evaluate import get_metrics, get_feature_config

router = APIRouter(prefix="/api/model", tags=["model"])


@router.get("/metrics")
async def metrics():
    try:
        m = get_metrics()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return {
        "accuracy": round(m["accuracy"], 4),
        "precision": round(m["precision"], 4),
        "recall": round(m["recall"], 4),
        "f1_score": round(m["f1_score"], 4),
        "confusion_matrix": m["confusion_matrix"],
        "num_classes": m["num_classes"],
        "test_set_size": m["test_set_size"],
    }


@router.get("/info")
async def info():
    try:
        cfg = get_feature_config()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return {
        "feature_columns": cfg["feature_columns"],
        "target_col": cfg["target_col"],
        "num_classes": cfg["num_classes"],
        "class_labels": cfg["class_labels"],
        "architecture": [
            "Input", "Dense(64, relu)", "Dropout(0.3)",
            "Dense(32, relu)", "Dropout(0.2)", "Output (softmax/sigmoid)",
        ],
    }
