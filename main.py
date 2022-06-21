from fastapi import FastAPI
from app.routers import recipes

app = FastAPI(
    title='Recipe API'
)


@app.get('/')
def root() -> dict:
    """Root GET"""
    return {"message": 'Hello World!'}


app.include_router(recipes.router)

