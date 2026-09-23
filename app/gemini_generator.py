from .config import DEMO_MODE, GEMINI_PRO_MODEL
from .demo_generator import generate_demo_plan
from .gemini_client import get_client


SYSTEM = """You are FitBuddy, a general wellness workout-plan assistant.
Create practical, conservative exercise guidance.
Do not diagnose conditions or prescribe treatment.
Respect the requested intensity.
Include rest and recovery.
Do not claim the plan is medically personalized.
Return plain text with exactly seven day sections and clear
warm-up, main workout, and cooldown/recovery sections.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:

    if DEMO_MODE or get_client() is None:
        return generate_demo_plan(username, goal, intensity)

    prompt = f"""{SYSTEM}

Create a 7-day workout plan for:

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

For each day provide:
- Focus
- 5–10 minute warm-up
- Exercises with sets/reps or duration
- Rest guidance
- Cooldown/recovery

Include at least one recovery/rest day.

Keep the plan practical and easy to scan.
"""

    response = get_client().models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt,
        config={
            "temperature": 0.6,
            "max_output_tokens": 5000,
        },
    )

    return (response.text or "").strip()