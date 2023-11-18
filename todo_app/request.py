from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=4)
    description: str = Field(min_length=3, max_length=200)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Develop",
                "description": "Learn Scala programming",
                "priority": 4,
                "complete": False,
            }
        }
