import os
import sys
# sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRouter
from  ..core.category_database import foods
from .Models import ItemBase
from ..core.Kitchen import Inventory, Recipe, RecipeBook
from ..core.Items import Item, CountableItem
import KitchenInventory.server.errors as err
from http import HTTPStatus

recipe_book_router = APIRouter()

inventory: Inventory
CURR_DIR = os.getcwd()


@recipe_book_router.get("/")
async def root():
    return {"msg": "Recipe Book! Do things here"}
