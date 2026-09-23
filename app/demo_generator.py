from textwrap import dedent

GOAL_FOCUS = {
    "weight loss": "moderate cardio and full-body strength with sustainable pacing",
    "muscle gain": "progressive resistance training with adequate recovery",
    "general wellness": "balanced strength, mobility, cardio and recovery",
    "flexibility": "mobility, stretching and controlled full-body movement",
}

def generate_demo_plan(username: str, goal: str, intensity: str) -> str:
    focus = GOAL_FOCUS.get(goal, "balanced fitness and recovery")
    days = [
        ("Day 1", "Full Body Strength"), ("Day 2", "Cardio + Core"),
        ("Day 3", "Mobility / Recovery"), ("Day 4", "Upper Body"),
        ("Day 5", "Lower Body"), ("Day 6", "Full Body + Light Cardio"),
        ("Day 7", "Rest / Gentle Walk"),
    ]
    blocks = []
    for day, focus_day in days:
        if focus_day.startswith("Rest"):
            body = "20–30 min easy walk if comfortable. Otherwise rest."
        elif focus_day.startswith("Mobility"):
            body = "Cat-cow 2×8, hip mobility 2×8/side, hamstring stretch 2×30s, shoulder mobility 2×8."
        elif "Cardio" in focus_day:
            body = "Brisk walk/cycle 20–30 min + plank 3×20–40s + dead bug 3×8/side."
        elif focus_day == "Upper Body":
            body = "Incline push-up 3×8–12, row 3×10–12, shoulder press 3×8–12, biceps curl 2×10–12."
        elif focus_day == "Lower Body":
            body = "Squat 3×8–12, reverse lunge 3×8/side, glute bridge 3×12–15, calf raise 2×15."
        else:
            body = "Squat 3×8–12, push-up 3×8–12, row 3×10–12, glute bridge 3×12–15."
        blocks.append(f"{day} — {focus_day}\nWarm-up: 5–10 min easy movement.\nMain: {body}\nCooldown: 5 min easy movement and comfortable stretching.")
    return dedent(f"""\
    FitBuddy demo plan for {username}
    Goal: {goal} | Intensity: {intensity}
    Focus: {focus}

    """ + "\n\n".join(blocks))

def generate_demo_tip(goal: str) -> str:
    tips = {
        "weight loss": "Prioritize regular meals built around vegetables, a protein source, whole-food carbohydrates and adequate water. Sustainable habits matter more than extreme restriction.",
        "muscle gain": "Include a protein-rich food in each main meal and eat enough overall to support training and recovery.",
        "flexibility": "Stay hydrated and pair mobility work with regular movement breaks rather than relying only on one long stretching session.",
        "general wellness": "Build meals around minimally processed foods, include protein and produce regularly, and keep hydration consistent.",
    }
    return tips.get(goal, tips["general wellness"])
