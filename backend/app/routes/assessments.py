from fastapi import APIRouter, Depends, HTTPException

from app.database.mongodb import recommendations_collection
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/{assessment_id}")
async def get_recommendations(assessment_id: str, current_user: dict = Depends(get_current_user)):
    doc = await recommendations_collection().find_one({"assessment_id": assessment_id})
    if not doc:
        raise HTTPException(status_code=404, detail="No recommendations found for this assessment")
    return {"assessment_id": assessment_id, "recommendations": doc["recommendations"]}
