from datetime import datetime, timezone

from bson import ObjectId

from app.database.mongodb import assessments_collection, recommendations_collection
from app.ml.predict import predict_stress
from app.services.recommendation_service import build_recommendations, get_age_group

LEVEL_NAMES = {0: "Low", 1: "Moderate", 2: "High"}


async def run_prediction_and_store(user_id: str, answers: dict) -> dict:
    result = predict_stress(answers)
    age_group = get_age_group(int(answers.get("age", 0)))
    level_name = LEVEL_NAMES.get(result["predicted_label"], str(result["predicted_label"]))

    recs = build_recommendations(answers, result["predicted_label"], result["stress_score"])

    now = datetime.now(timezone.utc)
    assessment_doc = {
        "user_id": user_id,
        "age": answers.get("age"),
        "age_group": age_group,
        "answers": answers,
        "prediction": level_name,
        "stress_score": result["stress_score"],
        "probabilities": result["probabilities"],
        "created_at": now,
    }
    insert_result = await assessments_collection().insert_one(assessment_doc)
    assessment_id = str(insert_result.inserted_id)

    await recommendations_collection().insert_one({
        "assessment_id": assessment_id,
        "recommendations": recs,
        "created_at": now,
    })

    return {
        "id": assessment_id,
        "predicted_label": level_name,
        "stress_score": result["stress_score"],
        "probabilities": result["probabilities"],
        "age_group": age_group,
        "created_at": now.isoformat(),
        "recommendations": recs,
    }


async def get_history(user_id: str) -> list[dict]:
    cursor = assessments_collection().find({"user_id": user_id}).sort("created_at", -1)
    items = []
    async for doc in cursor:
        items.append({
            "id": str(doc["_id"]),
            "age": doc.get("age"),
            "age_group": doc.get("age_group"),
            "prediction": doc.get("prediction"),
            "stress_score": doc.get("stress_score"),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
        })
    return items


async def get_assessment_by_id(assessment_id: str) -> dict | None:
    doc = await assessments_collection().find_one({"_id": ObjectId(assessment_id)})
    if not doc:
        return None
    doc["id"] = str(doc.pop("_id"))
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc
