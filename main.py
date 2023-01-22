from fastapi import FastAPI

from api.routes import auth, posts, scores

app = FastAPI()

app.include_router(auth.router, tags=['auth'])
app.include_router(posts.router, tags=['posts'])
app.include_router(scores.router, tags=['scores'])
