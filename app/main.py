from fastapi import FastAPI
from routers import auth  # Убрали app.

app = FastAPI(title="Restaurant Network API")

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Restaurant API"}