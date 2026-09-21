"""
train.py
--------
Phase 3-5 of the project: build the preprocessing pipeline, train a real
Deep Learning (MLP) model on StressLevelDataset.csv, evaluate it honestly,
and save every artifact the FastAPI backend needs for inference.

Run:
    cd backend
    python -m app.ml.train

Produces (in backend/models/):
    stress_model.keras
    scaler.pkl
    encoders.pkl
    feature_config.json
    metrics.json   (accuracy / precision / recall / f1 / confusion matrix -
                     read verbatim by GET /api/model/metrics, never hardcoded)
"""
import json
import os
import pickle

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from app.ml.preprocess import (
    load_dataset,
    inspect_dataset,
    detect_target_column,
    clean_dataset,
    build_preprocessing,
    save_feature_config,
    MODELS_DIR,
)


def build_model(input_dim: int, num_classes: int):
    """Dense -> ReLU -> Dropout -> Dense -> ReLU -> Dropout -> Output,
    per the architecture required by the project spec. Output activation
    is chosen from the ACTUAL number of classes discovered in the data,
    never assumed."""
    import tensorflow as tf
    from tensorflow.keras import layers, models

    output_units = 1 if num_classes == 2 else num_classes
    output_activation = "sigmoid" if num_classes == 2 else "softmax"
    loss = "binary_crossentropy" if num_classes == 2 else "sparse_categorical_crossentropy"

    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(32, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(output_units, activation=output_activation),
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss=loss,
        metrics=["accuracy"],
    )
    return model, loss


def main():
    print("Loading dataset...")
    df = load_dataset()

    report = inspect_dataset(df)
    print("Dataset inspection:", json.dumps({k: v for k, v in report.items() if k != "dtypes"}, default=str, indent=2))

    target_col = detect_target_column(df)
    print(f"Detected target column: {target_col}")

    df = clean_dataset(df)
    bundle = build_preprocessing(df, target_col)
    feature_config = save_feature_config(bundle)
    print("Feature config:", feature_config)

    os.makedirs(MODELS_DIR, exist_ok=True)

    import tensorflow as tf
    from tensorflow.keras.callbacks import EarlyStopping

    model, loss = build_model(bundle["X_train"].shape[1], bundle["num_classes"])
    model.summary()

    early_stop = EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True)

    model.fit(
        bundle["X_train"], bundle["y_train"],
        validation_data=(bundle["X_val"], bundle["y_val"]),
        epochs=100,
        batch_size=32,
        callbacks=[early_stop],
        verbose=2,
    )

    # ---- Real evaluation on held-out test set (never fabricated) ----
    if bundle["num_classes"] == 2:
        probs = model.predict(bundle["X_test"]).ravel()
        preds = (probs >= 0.5).astype(int)
    else:
        probs = model.predict(bundle["X_test"])
        preds = np.argmax(probs, axis=1)

    y_test = bundle["y_test"]
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_test, preds, average="weighted", zero_division=0)),
        "f1_score": float(f1_score(y_test, preds, average="weighted", zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
        "classification_report": classification_report(y_test, preds, zero_division=0),
        "num_classes": bundle["num_classes"],
        "test_set_size": int(len(y_test)),
    }
    print("Test metrics:", json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))
    print(metrics["classification_report"])

    # ---- Save all artifacts ----
    model.save(os.path.join(MODELS_DIR, "stress_model.keras"))
    with open(os.path.join(MODELS_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(bundle["scaler"], f)
    with open(os.path.join(MODELS_DIR, "encoders.pkl"), "wb") as f:
        pickle.dump({"feature_encoders": bundle["encoders"], "label_encoder": bundle["label_encoder"]}, f)
    with open(os.path.join(MODELS_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Artifacts saved to {MODELS_DIR}")


if __name__ == "__main__":
    main()
