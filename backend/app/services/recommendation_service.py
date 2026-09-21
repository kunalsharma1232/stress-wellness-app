"""
recommendation_service.py
--------------------------
Rule-based (intentionally - this is post-prediction guidance, not the
stress classification itself, which comes only from the trained model in
app/ml/predict.py). Recommendations depend on the individual factor scores
so two people with the same overall stress score can get different advice.
"""

AGE_GROUPS = [
    (10, 19), (20, 29), (30, 39), (40, 49), (50, 59),
    (60, 69), (70, 79), (80, 89), (90, 200),
]


def get_age_group(age: int) -> str:
    for lo, hi in AGE_GROUPS:
        if lo <= age <= hi:
            return f"{lo}-{hi}" if hi < 200 else "90+"
    return "unknown"


def build_recommendations(answers: dict, predicted_label, stress_score: float) -> list[str]:
    recs: list[str] = []

    if answers.get("sleep_quality", 3) <= 2:
        recs.append("Maintain a consistent sleep schedule and reduce screen exposure before bedtime.")

    if answers.get("anxiety_level", 0) >= 12:
        recs.append("Try slow breathing exercises, mindfulness, and short breaks during stressful activities.")

    if answers.get("headache", 0) >= 3 or answers.get("breathing_problem", 0) >= 3:
        recs.append("Consider discussing persistent or severe physical symptoms with a qualified healthcare professional.")

    if answers.get("depression", 0) >= 15:
        recs.append("Talking to a counselor or trusted person about how you're feeling can help - you don't have to manage this alone.")

    if answers.get("social_support", 3) <= 2:
        recs.append("Reaching out to friends, family, or a support group even briefly each day can ease feelings of isolation.")

    if answers.get("study_load", 0) >= 4 or answers.get("future_career_concerns", 0) >= 4:
        recs.append("Break large tasks into smaller steps and schedule short, regular breaks to reduce academic/career pressure.")

    if answers.get("living_conditions", 3) <= 2 or answers.get("safety", 3) <= 2:
        recs.append("If your living environment feels unsafe or unstable, consider speaking with a school counselor, HR, or a local support service.")

    if answers.get("bullying", 0) >= 3:
        recs.append("If bullying is affecting you, tell a trusted adult, teacher, or counselor - you deserve a safe environment.")

    if not recs:
        recs.append("Your responses don't show major risk factors right now - keep up habits like regular sleep, movement, and social connection.")

    if stress_score >= 80:
        recs.append("Your overall score is on the higher end - if this persists or feels overwhelming, please consider contacting a healthcare professional or counselor.")

    return recs
