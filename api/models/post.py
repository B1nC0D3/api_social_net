from fastapi import Depends
from pydantic import BaseModel, Field, validator

from api.models.auth import User
from services.auth import get_current_user


class BasePost(BaseModel):
    text: str = Field(..., max_length=1024)


class PostCreate(BasePost):
    pass


class PostResponse(BasePost):
    id: int
    author_id: int
    likes: int
    dislikes: int
    is_author: bool

    class Config:
        orm_mode = True
