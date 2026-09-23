from .config import DEMO_MODE, GEMINI_PRO_MODEL
from .demo_generator import generate_demo_plan
from .gemini_client import get_client

def update_workout_plan(original_plan: str, feedback: str, username: str, goal: str, intensity: str) -> str:
    if DEMO_MODE or get_client() is None:
        return original_plan + f"\n\nFeedback applied: {feedback}\n\nAdjustment: Keep the same weekly structure while applying the requested preference where practical and preserving recovery."
    prompt = f"""You are FitBuddy. Revise the workout plan below using the user's feedback. Preserve useful structure, goal alignment and recovery. Do not provide medical treatment. Return the complete revised 7-day plan, not a diff.\n\nUser: {username}\nGoal: {goal}\nIntensity: {intensity}\n\nORIGINAL PLAN:\n{original_plan}\n\nUSER FEEDBACK:\n{feedback}"""
    response = get_client().models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt,
        config={"temperature": 0.6, "max_output_tokens": 5000},
    )
    return (response.text or "").strip()
