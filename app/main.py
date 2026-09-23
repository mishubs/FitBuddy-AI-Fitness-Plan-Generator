from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router

init_db()

app = FastAPI(title="FitBuddy — AI Fitness Plan Generator", version="1.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()
