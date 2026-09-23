from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
    username: str = Field(min_length=1, max_length=120)
    user_id: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=500)
    goal: str = Field(min_length=2, max_length=50)
    intensity: str = Field(min_length=3, max_length=20)

    @field_validator("goal", "intensity", mode="before")
    @classmethod
    def clean_text(cls, value):
        return str(value).strip().lower()

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=100)
    feedback: str = Field(min_length=3, max_length=2000)
