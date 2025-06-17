from fastapi import FastAPI
from .inventory_routes import inventory_router
from .recipe_book_routes import recipe_book_router
from ..core.category_database import foods
app = FastAPI()

app.include_router(inventory_router, prefix="/v1/inventory", tags=["inventory"])
app.include_router(recipe_book_router, prefix="/v1/recipe-book", tags=["recipe-book"])


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