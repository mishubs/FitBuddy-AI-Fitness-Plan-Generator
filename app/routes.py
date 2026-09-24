
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .models import Plan, User
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_user_and_plan(db: Session, user_id: str):
    user = db.scalar(
        select(User).where(User.user_id == user_id)
    )

    plan = db.scalar(
        select(Plan)
        .where(Plan.user_id == user_id)
        .order_by(Plan.id.desc())
    )

    return user, plan


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        existing = db.scalar(
            select(User).where(User.user_id == data.user_id)
        )

        if existing:
            existing.username = data.username
            existing.age = data.age
            existing.weight = data.weight
            existing.goal = data.goal
            existing.intensity = data.intensity

            user = existing

            old_plan = db.scalar(
                select(Plan)
                .where(Plan.user_id == data.user_id)
                .order_by(Plan.id.desc())
            )

            if old_plan:
                db.delete(old_plan)
                db.flush()

        else:
            user = User(**data.model_dump())
            db.add(user)
            db.flush()

        workout = generate_workout_gemini(
            data.username,
            data.age,
            data.weight,
            data.goal,
            data.intensity,
        )

        tip = generate_nutrition_tip_with_flash(data.goal)

        plan = Plan(
            user_id=data.user_id,
            original_plan=workout,
            nutrition_tip=tip,
        )

        db.add(plan)
        db.commit()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan,
                "message": None,
                "error": None,
            },
        )

    except Exception as exc:
        db.rollback()

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"Could not generate the plan: {exc}"
            },
            status_code=500,
        )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        payload = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )

        user, plan = get_user_and_plan(
            db,
            payload.user_id,
        )

        if not user or not plan:
            raise HTTPException(
                status_code=404,
                detail="User or plan not found",
            )

        revised = update_workout_plan(
            plan.updated_plan or plan.original_plan,
            payload.feedback,
            user.username,
            user.goal,
            user.intensity,
        )

        plan.updated_plan = revised
        plan.feedback = payload.feedback
        plan.updated_nutrition_tip = generate_nutrition_tip_with_flash(
            user.goal
        )
        plan.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(plan)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan,
                "message": "Your plan has been updated using your feedback.",
                "error": None,
            },
        )

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Could not update plan: {exc}",
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db),
):
    users = db.scalars(
        select(User).order_by(User.id.desc())
    ).all()

    plans = db.scalars(
        select(Plan).order_by(Plan.id.desc())
    ).all()

    latest = {}

    for plan in plans:
        latest.setdefault(plan.user_id, plan)

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
            "plans": latest,
        },
    )


@router.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "FitBuddy",
    }


@router.post("/api/generate-workout")
def api_generate(
    payload: UserInput,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.user_id == payload.user_id)
    )

    if not user:
        user = User(**payload.model_dump())
        db.add(user)

    else:
        for key, value in payload.model_dump().items():
            setattr(user, key, value)

    workout = generate_workout_gemini(
        payload.username,
        payload.age,
        payload.weight,
        payload.goal,
        payload.intensity,
    )

    tip = generate_nutrition_tip_with_flash(
        payload.goal
    )

    plan = Plan(
        user_id=payload.user_id,
        original_plan=workout,
        nutrition_tip=tip,
    )

    db.add(plan)
    db.commit()

    return {
        "user": payload.model_dump(),
        "workout_plan": workout,
        "nutrition_tip": tip,
    }


@router.post("/api/submit-feedback")
def api_feedback(
    payload: FeedbackRequest,
    db: Session = Depends(get_db),
):
    user, plan = get_user_and_plan(
        db,
        payload.user_id,
    )

    if not user or not plan:
        raise HTTPException(
            status_code=404,
            detail="User or plan not found",
        )

    revised = update_workout_plan(
        plan.updated_plan or plan.original_plan,
        payload.feedback,
        user.username,
        user.goal,
        user.intensity,
    )

    plan.updated_plan = revised
    plan.feedback = payload.feedback
    plan.updated_nutrition_tip = generate_nutrition_tip_with_flash(
        user.goal
    )
    plan.updated_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "user_id": user.user_id,
        "updated_plan": revised,
        "nutrition_tip": plan.updated_nutrition_tip,
    }


@router.get("/api/users")
def api_users(
    db: Session = Depends(get_db),
):
    users = db.scalars(
        select(User).order_by(User.id.desc())
    ).all()

    return [
        {
            "user_id": u.user_id,
            "username": u.username,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
        }
        for u in users
    ]


@router.get("/api/users/{user_id}")
def api_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    user, plan = get_user_and_plan(
        db,
        user_id,
    )

    if not user or not plan:
        raise HTTPException(
            status_code=404,
            detail="User or plan not found",
        )

    return {
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
        },
        "original_plan": plan.original_plan,
        "updated_plan": plan.updated_plan,
        "nutrition_tip": plan.nutrition_tip,
        "updated_nutrition_tip": plan.updated_nutrition_tip,
        "feedback": plan.feedback,
    }
    