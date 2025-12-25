from fastapi import FastAPI
from routers import auth, restaurant

app = FastAPI(title="Restaurant Network API")

app.include_router(auth.router)
app.include_router(restaurant.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Restaurant API"}