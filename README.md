# FitBuddy — AI Fitness Plan Generator

A FastAPI + Jinja2 + SQLite application that follows the supplied FitBuddy project specification: personalized 7-day workout plans, nutrition/recovery tips, feedback-based plan updates, and an all-users admin view.

## Important implementation note
The supplied document names Gemini 1.5 Pro and Gemini Flash. Those model names are legacy relative to the current Gemini API. This implementation uses the current `google-genai` SDK and configurable stable model IDs (`gemini-2.5-pro` and `gemini-2.5-flash`) by default. The model IDs can be changed in `.env` without changing application code.

## Features
- User form: name, user ID, age, weight, goal, intensity.
- AI-generated 7-day workout plan.
- AI-generated nutrition/recovery tip.
- Feedback-based workout-plan regeneration.
- SQLite persistence with SQLAlchemy.
- Admin-style `/view-all-users` page.
- JSON API endpoints under `/api`.
- Automatic local demo mode when no Gemini key is available, so the UI can be tested before configuring AI.
- Responsive frontend with no external frontend build step.

## Project structure
```text
fitbuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── demo_generator.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   └── all_users.html
│   └── static/
│       └── style.css
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start — Windows / VS Code
1. Open this folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:
   `python -m venv .venv`
4. Activate it:
   ` .venv\Scripts\activate`
   If that command was copied incorrectly, use:
   `.venv\Scripts\activate`
5. Install packages:
   `pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `GEMINI_API_KEY`.
8. Start the server:
   `uvicorn app.main:app --reload`
9. Open `http://127.0.0.1:8000`.
10. API docs: `http://127.0.0.1:8000/docs`.

### Run without an API key
Set `DEMO_MODE=true` in `.env`, or simply leave the key empty. The application will use a deterministic local demo generator. This verifies the frontend, routes and database without consuming Gemini API quota.

## API endpoints
- `GET /api/health`
- `POST /api/generate-workout`
- `POST /api/submit-feedback`
- `GET /api/users`
- `GET /api/users/{user_id}`

The browser UI uses the same service layer as the API routes.

## Testing checklist
1. Submit a new user from the home page.
2. Confirm a result page shows the 7-day plan and nutrition tip.
3. Submit feedback such as `Add more cardio and one additional rest day.`
4. Confirm the updated plan is stored and displayed.
5. Open `/view-all-users` and confirm both original and updated plans are visible.
6. Open `/docs` and try `/api/health`.

## Safety note
FitBuddy generates general wellness/fitness suggestions, not medical diagnosis or individualized medical treatment. Users with injuries, medical conditions, pregnancy, or other health concerns should seek advice from an appropriately qualified professional before following an exercise or nutrition program.
