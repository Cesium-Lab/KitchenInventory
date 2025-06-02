from fastapi import FastAPI
from .inventory_routes import inventory_router
from ..category_database import foods
app = FastAPI()

app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])


# TODO: List commands that this app can do
@app.get("/")
async def root():
    return {"message": "Welcome to The server!"}

@app.get("/foods")
async def get_foods():
    return {
        "foods": foods()
    }

# recipe_book: RecipeBook = None