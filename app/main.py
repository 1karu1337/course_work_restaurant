from fastapi import FastAPI
from routers import auth, restaurant, table, menu, ingredient, order

app = FastAPI(title="Restaurant Network API")

app.include_router(auth.router)
app.include_router(restaurant.router)
app.include_router(table.router)
app.include_router(menu.router)
app.include_router(ingredient.router)
app.include_router(order.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Restaurant API"}