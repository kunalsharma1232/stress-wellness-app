# MindScope AI - Stress Level Prediction and Wellness Recommendation System

A B.Tech Artificial Intelligence & Data Science final-year project: a full-stack, AI-powered wellness
platform that predicts a user's stress level from a questionnaire using a trained Deep Learning model,
and returns personalized wellness recommendations.

---

## 1. Project Overview

MindScope AI collects apython -m app.ml.trainn age-appropriate questionnaire, maps the answers to a fixed set of numeric
features, runs them through a trained neural network, and returns a stress category, a normalized
0-100 "AI-derived stress score," the contributing factors, and personalized wellness guidance. An
optional NLP/GPT-style wellness assistant chat is also included, kept separate from the core prediction
model.

## 2. Problem Statement

Stress affects people across every age group, but is rarely measured or explained in an accessible,
personalized way. Most people only notice the scale of their stress after it has already affected
their health, relationships, or performance.

## 3. Objectives

- Predict a user's stress category using a genuinely trained Deep Learning model (no if/else rules).
- Adapt the questionnaire's wording to the user's age group while feeding a consistent feature set to the model.
- Provide personalized, explainable wellness recommendations.
- Visualize stress factors and history with real charts.
- Store user data and prediction history securely.

## 4. Features

- Age-aware, multi-step questionnaire with progress tracking and validation.
- Deep Learning (MLP neural network) stress classification with real, non-fabricated evaluation metrics.
- Stress Result page with a circular gauge, contributing factors, and a clear "not a medical diagnosis" disclaimer.
- Analytics page: factor bar chart, stress-history line chart, category distribution pie chart.
- Prediction history table with detail view.
- Personalized wellness recommendations, tailored to which specific factors are elevated.
- Optional NLP/GPT wellness assistant, kept separate from the prediction model, with a safety override for crisis language.
- JWT authentication with hashed passwords; protected routes; MongoDB storage.
- Fully responsive, modular CSS (no Tailwind).

## 5. Technology Stack

**Frontend:** React 18, TypeScript, React Router, Axios, Recharts, modular CSS, Vite.
**Backend:** Python, FastAPI, Pydantic, Uvicorn, Motor (async MongoDB), PyJWT, Passlib (bcrypt).
**AI/ML:** Pandas, NumPy, scikit-learn (preprocessing/evaluation), TensorFlow/Keras (Deep Learning MLP).
**Database:** MongoDB.

## 6. System Architecture

```
React + TypeScript SPA  <-- Axios/JWT -->  FastAPI REST API  <-->  MongoDB
                                                |
                                                v
                                 app/ml (preprocess, train, predict)
                                                |
                                                v
                                   stress_model.keras + scaler.pkl
```

## 7. AI Methodology

1. Inspect the raw CSV: shape, missing values, duplicates, dtypes, class balance.
2. Auto-detect the target column (no assumed labels).
3. Clean (drop duplicates/missing rows), encode any categorical columns, scale numeric features with `StandardScaler`.
4. Split into train / validation / test sets (stratified).
5. Train a Dense -> ReLU -> Dropout -> Dense -> ReLU -> Dropout -> Output MLP, with output activation
   (softmax or sigmoid) chosen from the *actual* number of classes found in the data, using Adam and
   early stopping on validation loss.
6. Evaluate on the held-out test set: accuracy, precision, recall, F1, confusion matrix - all computed,
   never hardcoded, and exposed verbatim via `GET /api/model/metrics`.
7. Save the model, scaler, encoders, and feature config for the FastAPI inference service.

## 8. Dataset

The pipeline expects `backend/dataset/StressLevelDataset.csv` with the (real, public) Kaggle "Student
Stress Factors" schema: `anxiety_level, self_esteem, mental_health_history, depression, headache,
blood_pressure, sleep_quality, breathing_problem, noise_level, living_conditions, safety, basic_needs,
academic_performance, study_load, teacher_student_relationship, future_career_concerns, social_support,
peer_pressure, extracurricular_activities, bullying, age, stress_level` (target, 3 classes: Low/Moderate/High).

> **Important - please read:** the environment this project was built in has no outbound network
> access, so the real Kaggle CSV could not be downloaded. `backend/dataset/generate_dataset.py`
> generates a locally-synthesized stand-in with the identical schema and genuine, deliberately-built
> correlations between features and the target, so the training pipeline has real signal to learn from
> and its metrics are real. **To use the authentic dataset:** download `StressLevelDataset.csv` from
> Kaggle and overwrite the file at `backend/dataset/StressLevelDataset.csv` - nothing else in the
> pipeline needs to change.

## 9. Deep Learning Model

See `backend/app/ml/train.py`. Architecture:

```
Input -> Dense(64, ReLU) -> Dropout(0.3) -> Dense(32, ReLU) -> Dropout(0.2) -> Output (softmax/sigmoid)
```

## 10. Model Evaluation

Running the full pipeline end-to-end (validated in this build using an equivalent scikit-learn MLP,
since TensorFlow could not be installed in the offline build sandbox) on the generated dataset produced:

| Metric | Value |
|---|---|
| Accuracy | ~87.9% |
| Precision (weighted) | ~87.8% |
| Recall (weighted) | ~87.9% |
| F1-score (weighted) | ~87.8% |

These numbers will change once you run `python -m app.ml.train` with TensorFlow installed and/or the
real Kaggle CSV in place - `GET /api/model/metrics` always reflects whatever `metrics.json` your own
training run produced, never a fixed value.

## 11. API Documentation

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Log in, returns JWT |
| GET | `/api/auth/me` | Current user |
| POST | `/api/predictions/predict` | Run the DL model on questionnaire answers |
| GET | `/api/predictions/history` | List past assessments |
| GET | `/api/predictions/{id}` | One assessment's detail |
| GET | `/api/analytics/summary` | Dashboard summary stats |
| GET | `/api/analytics/history` | Time series of stress scores |
| GET | `/api/recommendations/{assessment_id}` | Recommendations for one assessment |
| POST | `/api/chat` | NLP/GPT wellness assistant |
| GET | `/api/model/metrics` | Real model evaluation metrics |
| GET | `/api/model/info` | Feature columns, classes, architecture |

FastAPI also serves interactive docs at `/docs` once running.

## 12. MongoDB Structure

Database: `stress_wellness_db`. Collections: `users`, `assessments`, `recommendations`, `chatbot_sessions`
(see `backend/app/database/mongodb.py`). Passwords are always stored as bcrypt hashes, never plain text.

## 13. Installation

```bash
git clone <this-repo>
cd stress-wellness-app
```

## 14. Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in real values:

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=stress_wellness_db
JWT_SECRET=replace-with-a-long-random-string
OPENAI_API_KEY=   # optional - leave blank to use the offline wellness-assistant fallback
FRONTEND_ORIGIN=http://localhost:5173
```

## 15. Running the Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
.\venv\Scripts\Activate.ps1   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m app.ml.train          # trains the model, needed once before first run
uvicorn app.main:app --reload --port 8000
```Registration failed. Please try again.

## 16. Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`.

## 17. Screenshots

_Add screenshots of the Home, Questionnaire, Stress Result, Analytics, and AI Technology pages here
before submission._

## 18. Testing

See `docs/TESTING.md` for the manual test-case checklist covering registration, login, questionnaire
validation across age groups, the prediction API, database storage, history, graphs, recommendations,
the wellness assistant, mobile responsiveness, and backend error handling.

## 19. Limitations

- The shipped dataset is a locally-generated, schema-accurate stand-in - swap in the real Kaggle CSV for production-quality results.
- Self-reported questionnaire data can be subjective and is not clinically validated.
- The NLP wellness assistant falls back to simple keyword-based guidance if no `OPENAI_API_KEY` is configured.

## 20. Future Scope

- Retrain on larger, more diverse real-world datasets.
- Add explainability (e.g. SHAP) to show which factors drove a given prediction.
- Add email/SMS check-in reminders and richer longitudinal analytics.

## 21. Disclaimer

This application is designed for educational and wellness-support purposes. It does not provide
medical diagnosis or replace professional medical advice. If you or someone you know is experiencing
a mental-health emergency, please contact a qualified healthcare professional or emergency service
immediately.
