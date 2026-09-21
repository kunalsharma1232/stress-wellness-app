from fastapi import APIRouter, Depends, HTTPException

from app.models.assessment import QuestionnaireAnswers
from app.routes.auth import get_current_user
from app.services import prediction_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.post("/predict")
async def predict(payload: QuestionnaireAnswers, current_user: dict = Depends(get_current_user)):
    try:
        result = await prediction_service.run_prediction_and_store(
            user_id=str(current_user["_id"]), answers=payload.model_dump()
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return result


@router.get("/history")
async def history(current_user: dict = Depends(get_current_user)):
    return await prediction_service.get_history(str(current_user["_id"]))


@router.get("/{assessment_id}")
async def get_one(assessment_id: str, current_user: dict = Depends(get_current_user)):
    doc = await prediction_service.get_assessment_by_id(assessment_id)
    if not doc or doc.get("user_id") != str(current_user["_id"]):
        raise HTTPException(status_code=404, detail="Assessment not found")
    return doc
