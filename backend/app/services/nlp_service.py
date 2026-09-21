"""
nlp_service.py
---------------
The optional NLP/GPT wellness assistant (spec section 17). Deliberately
kept separate from the Deep Learning stress-prediction model - this module
never outputs a stress class or score, only supportive, non-diagnostic
wellness guidance.

If OPENAI_API_KEY is configured, messages are sent to the OpenAI API with a
strict system prompt. If not, a lightweight keyword-based NLP fallback
provides safe generic guidance so the feature still works in a fully
offline/dev setup - this fallback is clearly informational, not "real GPT",
and the AI Technology page should say so.
"""
from app.config import settings

SYSTEM_PROMPT = (
    "You are a supportive wellness assistant inside a student wellness app. "
    "You are NOT a doctor and must never diagnose any medical or mental health "
    "condition. Offer general, safe wellness guidance only: breathing exercises, "
    "study/work break suggestions, sleep hygiene tips, and mindfulness ideas. "
    "If the user describes severe distress, self-harm, or a crisis, gently "
    "encourage them to reach out to a trusted adult, counselor, or local "
    "emergency/crisis service right away, and keep your response brief and caring."
)

CRISIS_KEYWORDS = ["suicide", "kill myself", "end my life", "self harm", "self-harm", "hurt myself"]

FALLBACK_TIPS = {
    "exam": "Exams can bring on real pressure. Try breaking your revision into 25-minute focused blocks with short breaks (a Pomodoro-style approach), and make sure you're sleeping enough the nights before - tired brains retain less.",
    "sleep": "For better sleep: keep a consistent bedtime, dim screens an hour before bed, and try a short wind-down routine like light stretching or reading.",
    "work": "When work feels overwhelming, list tasks by priority, tackle the most important one first, and schedule real breaks - even 5 minutes away from the screen helps.",
    "anxious": "When anxiety spikes, a simple technique is slow breathing: inhale for 4 seconds, hold for 4, exhale for 6. Repeat a few times.",
    "lonely": "Feeling isolated is hard. Even a short message to a friend or family member, or joining a group activity, can help rebuild connection.",
}
DEFAULT_TIP = "It sounds like things feel heavy right now. Try a few slow breaths, take a short break from whatever's stressing you, and consider talking to someone you trust about how you're feeling."


def _contains_crisis_language(text: str) -> bool:
    lowered = text.lower()
    return any(k in lowered for k in CRISIS_KEYWORDS)


def _fallback_reply(message: str) -> str:
    lowered = message.lower()
    for keyword, tip in FALLBACK_TIPS.items():
        if keyword in lowered:
            return tip
    return DEFAULT_TIP


def get_wellness_reply(message: str) -> dict:
    if _contains_crisis_language(message):
        return {
            "reply": (
                "I'm really glad you told me this. I can't provide the support you "
                "need for something this serious, but please reach out right now to "
                "a trusted adult, a counselor, or your local emergency/crisis line - "
                "you deserve immediate, real support."
            ),
            "source": "safety_override",
        }

    if settings.OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                max_tokens=300,
            )
            return {"reply": completion.choices[0].message.content, "source": "gpt"}
        except Exception:
            # Fall through to the offline fallback rather than failing the request
            pass

    return {"reply": _fallback_reply(message), "source": "nlp_fallback"}
