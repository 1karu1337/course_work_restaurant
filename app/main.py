from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import auth, restaurant, table, menu, ingredient, order, export, admin

app = FastAPI(title="Restaurant Network API")

app.include_router(auth.router)
app.include_router(restaurant.router)
app.include_router(table.router)
app.include_router(menu.router)
app.include_router(ingredient.router)
app.include_router(order.router)
app.include_router(export.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("../static/index.html")