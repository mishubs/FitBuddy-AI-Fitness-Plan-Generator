from .config import DEMO_MODE, GEMINI_FLASH_MODEL
from .demo_generator import generate_demo_tip
from .gemini_client import get_client

def generate_nutrition_tip_with_flash(goal: str) -> str:
    if DEMO_MODE or get_client() is None:
        return generate_demo_tip(goal)
    prompt = f"Give one concise, practical general nutrition or recovery tip for a person whose fitness goal is {goal}. Mention a food/hydration/recovery action. Avoid medical treatment claims and extreme dieting. Maximum 100 words."
    response = get_client().models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt,
        config={"temperature": 0.5, "max_output_tokens": 300},
    )
    return (response.text or "").strip()
