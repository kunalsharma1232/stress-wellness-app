from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routes import auth, predictions, assessments, analytics, chatbot, model

app = FastAPI(
    title="AI Based Stress Level Prediction and Wellness Recommendation System",
    description="Backend API: Deep Learning stress prediction, wellness recommendations, and an NLP wellness assistant.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predictions.router)
app.include_router(assessments.router)
app.include_router(analytics.router)
app.include_router(chatbot.router)
app.include_router(model.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


@app.get("/")
async def root():
    return {
        "status": "ok",
        "name": "AI Based Stress Level Prediction and Wellness Recommendation System API",
        "disclaimer": "Educational/wellness-support system - not a medical diagnosis tool.",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
