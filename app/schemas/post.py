from pydantic import BaseModel
from typing import List
from datetime import datetime

class OptionCreate(BaseModel):
    text: str

class PostCreate(BaseModel):
    title: str
    category: str
    options: List[OptionCreate]

class OptionOut(OptionCreate):
    id: int

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    id: int
    title: str
    category: str
    created_at: datetime
    options: List[OptionOut]

    class Config:
        orm_mode = True
