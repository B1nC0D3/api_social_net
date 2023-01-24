from pydantic import BaseModel


class ScoresResponse(BaseModel):
    likes: int
    dislikes: int

    class Config:
        orm_mode = True
