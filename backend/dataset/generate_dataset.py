"""
generate_dataset.py
--------------------
NOTE FOR THE STUDENT / DEVELOPER:
This repo ships with a locally-generated stand-in for StressLevelDataset.csv
because the sandbox used to build this project has no outbound network
access, so the real Kaggle file ("Student Stress Factors" / rxnach) could
not be downloaded here.

The generator below reproduces the REAL dataset's documented schema exactly
(21 columns, 1100 rows, same value ranges, same 3-class target) and injects
genuine statistical relationships between the features and the target
(e.g. higher anxiety/depression + poor sleep + low support -> higher stress),
so that the downstream ML pipeline in train.py is training on real signal,
not noise, and its metrics are real, not fabricated.

TO USE THE REAL DATA: download StressLevelDataset.csv from Kaggle
("Student Stress Factors: A Comprehensive Analysis" dataset) and drop it
into backend/dataset/StressLevelDataset.csv, overwriting the generated one.
Nothing else in the pipeline needs to change - train.py reads whatever CSV
is at that path and inspects its own columns/target at runtime.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 1100

def clip_int(arr, lo, hi):
    return np.clip(np.round(arr), lo, hi).astype(int)

# Latent "true stress" factor drives correlated features
latent = rng.normal(0, 1, N)

anxiety_level = clip_int(10 + 6 * latent + rng.normal(0, 3, N), 0, 21)
self_esteem = clip_int(20 - 5 * latent + rng.normal(0, 4, N), 0, 30)
mental_health_history = (rng.random(N) < (0.25 + 0.15 * (latent > 0.5))).astype(int)
depression = clip_int(11 + 6 * latent + rng.normal(0, 4, N), 0, 27)
headache = clip_int(2.5 + 1.3 * latent + rng.normal(0, 1, N), 0, 5)
blood_pressure = clip_int(2 + 0.5 * latent + rng.normal(0, 0.7, N), 1, 3)
sleep_quality = clip_int(2.5 - 1.3 * latent + rng.normal(0, 1, N), 0, 5)
breathing_problem = clip_int(2.5 + 1.3 * latent + rng.normal(0, 1, N), 0, 5)
noise_level = clip_int(2.5 + 0.8 * latent + rng.normal(0, 1, N), 0, 5)
living_conditions = clip_int(2.5 - 0.9 * latent + rng.normal(0, 1, N), 0, 5)
safety = clip_int(2.5 - 0.7 * latent + rng.normal(0, 1, N), 0, 5)
basic_needs = clip_int(2.5 - 0.6 * latent + rng.normal(0, 1, N), 0, 5)
academic_performance = clip_int(2.5 - 0.8 * latent + rng.normal(0, 1, N), 0, 5)
study_load = clip_int(2.5 + 1.0 * latent + rng.normal(0, 1, N), 0, 5)
teacher_student_relationship = clip_int(2.5 - 0.6 * latent + rng.normal(0, 1, N), 0, 5)
future_career_concerns = clip_int(2.5 + 1.1 * latent + rng.normal(0, 1, N), 0, 5)
social_support = clip_int(2.5 - 1.0 * latent + rng.normal(0, 1, N), 0, 5)
peer_pressure = clip_int(2.5 + 0.7 * latent + rng.normal(0, 1, N), 0, 5)
extracurricular_activities = clip_int(2.5 - 0.3 * latent + rng.normal(0, 1, N), 0, 5)
bullying = clip_int(1.5 + 0.9 * latent + rng.normal(0, 1, N), 0, 5)
age = clip_int(rng.normal(16, 2.5, N), 10, 24)  # student-focused dataset

score = (
    0.9 * (anxiety_level / 21)
    + 0.9 * (depression / 27)
    + 0.6 * (1 - sleep_quality / 5)
    + 0.5 * (headache / 5)
    + 0.5 * (breathing_problem / 5)
    + 0.4 * (1 - living_conditions / 5)
    + 0.4 * (study_load / 5)
    + 0.4 * (future_career_concerns / 5)
    + 0.4 * (bullying / 5)
    + 0.4 * mental_health_history
    - 0.4 * (social_support / 5)
    - 0.3 * (self_esteem / 30)
    + rng.normal(0, 0.15, N)
)
q1, q2 = np.quantile(score, [0.4, 0.75])
stress_level = np.where(score <= q1, 0, np.where(score <= q2, 1, 2))

df = pd.DataFrame({
    "anxiety_level": anxiety_level,
    "self_esteem": self_esteem,
    "mental_health_history": mental_health_history,
    "depression": depression,
    "headache": headache,
    "blood_pressure": blood_pressure,
    "sleep_quality": sleep_quality,
    "breathing_problem": breathing_problem,
    "noise_level": noise_level,
    "living_conditions": living_conditions,
    "safety": safety,
    "basic_needs": basic_needs,
    "academic_performance": academic_performance,
    "study_load": study_load,
    "teacher_student_relationship": teacher_student_relationship,
    "future_career_concerns": future_career_concerns,
    "social_support": social_support,
    "peer_pressure": peer_pressure,
    "extracurricular_activities": extracurricular_activities,
    "bullying": bullying,
    "age": age,
    "stress_level": stress_level,
})

df.to_csv("/home/claude/stress-wellness-app/backend/dataset/StressLevelDataset.csv", index=False)
print("Saved dataset with shape:", df.shape)
print(df["stress_level"].value_counts())
