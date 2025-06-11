from pydantic import BaseModel

class VoteCreate(BaseModel):
    option_id: int
