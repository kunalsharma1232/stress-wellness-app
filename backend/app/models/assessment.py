from typing import Optional
from pydantic import BaseModel, Field


class QuestionnaireAnswers(BaseModel):
    """Core ML feature set. Every age-group questionnaire in the frontend
    maps its (age-appropriate wording) answers down to these same fields
    before they ever reach the API - see AGE_GROUP_QUESTIONS mapping in the
    frontend and FEATURE_MAP notes in recommendation_service.py."""
    age: int = Field(..., ge=10, le=110)
    anxiety_level: float = Field(..., ge=0, le=21)
    self_esteem: float = Field(0, ge=0, le=30)
    mental_health_history: int = Field(..., ge=0, le=1)
    depression: float = Field(..., ge=0, le=27)
    headache: float = Field(..., ge=0, le=5)
    blood_pressure: float = Field(2, ge=1, le=3)
    sleep_quality: float = Field(..., ge=0, le=5)
    breathing_problem: float = Field(..., ge=0, le=5)
    noise_level: float = Field(2, ge=0, le=5)
    living_conditions: float = Field(..., ge=0, le=5)
    safety: float = Field(2, ge=0, le=5)
    basic_needs: float = Field(2, ge=0, le=5)
    academic_performance: float = Field(2, ge=0, le=5)
    study_load: float = Field(2, ge=0, le=5)
    teacher_student_relationship: float = Field(2, ge=0, le=5)
    future_career_concerns: float = Field(2, ge=0, le=5)
    social_support: float = Field(2, ge=0, le=5)
    peer_pressure: float = Field(2, ge=0, le=5)
    extracurricular_activities: float = Field(2, ge=0, le=5)
    bullying: float = Field(0, ge=0, le=5)


class PredictionResponse(BaseModel):
    id: Optional[str] = None
    predicted_label: str
    stress_score: float
    probabilities: dict
    age_group: str
    created_at: Optional[str] = None
