from fastapi import APIRouter, Depends

from app.database.mongodb import assessments_collection
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary")
async def summary(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    cursor = assessments_collection().find({"user_id": user_id}).sort("created_at", -1)
    docs = [d async for d in cursor]

    if not docs:
        return {"has_data": False}

    latest = docs[0]
    distribution = {"Low": 0, "Moderate": 0, "High": 0}
    for d in docs:
        distribution[d.get("prediction", "Low")] = distribution.get(d.get("prediction", "Low"), 0) + 1

    factor_keys = ["anxiety_level", "depression", "sleep_quality", "headache", "breathing_problem"]
    factor_totals = {k: 0 for k in factor_keys}
    for d in docs:
        for k in factor_keys:
            factor_totals[k] += d.get("answers", {}).get(k, 0)
    factor_avg = {k: round(v / len(docs), 2) for k, v in factor_totals.items()}

    return {
        "has_data": True,
        "latest_score": latest.get("stress_score"),
        "latest_level": latest.get("prediction"),
        "total_assessments": len(docs),
        "category_distribution": distribution,
        "factor_averages": factor_avg,
    }


@router.get("/history")
async def history(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    cursor = assessments_collection().find({"user_id": user_id}).sort("created_at", 1)
    points = []
    async for d in cursor:
        points.append({
            "date": d["created_at"].isoformat() if d.get("created_at") else None,
            "stress_score": d.get("stress_score"),
            "level": d.get("prediction"),
        })
    return points
