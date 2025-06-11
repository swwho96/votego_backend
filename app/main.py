from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import post as post_router
from .routers import vote as vote_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VoteGo MVP")

app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
app.include_router(vote_router.router, prefix="/votes", tags=["Votes"])
