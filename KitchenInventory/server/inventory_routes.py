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

inventory_router = APIRouter()

inventory: Inventory
CURR_DIR = os.getcwd()


@inventory_router.get("/")
async def root():
    return {"msg": "Inventory! Do things here"}

########################################################################
#                                Loading                               #
########################################################################
    
@inventory_router.get("/list") # tested
async def get_inventory_numbers():
    directories = os.listdir(f"{CURR_DIR}/inventories")
    strings = [(i,directory) for i,directory in enumerate(directories)]
    return {
        "inventories": strings
    }

@inventory_router.put("/select") # tested
async def select_inventory(num: int):
    global inventory
    directories = os.listdir(f"{CURR_DIR}/inventories")
    if num < 0 or num >= len(directories):
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                             detail=f"'{num}' out of range of inventory numbers (0-{len(directories)-1} inclusive)")
    
    try:
        inventory = Inventory.load(f"{CURR_DIR}/inventories/{directories[num]}")
    except Exception as e:
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                             detail=str(e))
    return {"msg": f"Loaded '{directories[num]}' into Inventory '{inventory.name}'"}
    
@inventory_router.put("/create") # tested
async def create_inventory(name: str):
    global inventory
    directories = os.listdir(f"{CURR_DIR}/inventories")
    for i, inv_name in enumerate(directories):
        if f"{name}.csv" == inv_name:
            await select_inventory(i)
            return {"msg": f"Found '{directories[i]}' and loaded into Inventory '{inventory.name}'"}

    inventory = Inventory(name)
    return {"msg": f"Created Inventory '{inventory.name}'"}

########################################################################
#                                  Items                               #
########################################################################

@inventory_router.post("/add-item") # TODO: finish and test
async def add_item(item_base: ItemBase):
    if inventory is None:
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                            detail="Inventory not loaded")       
    try:
        item = item_base.to_Item()
    except Exception as e:
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                             detail=str(e))
    
    # Add to item if already existsh

    try:
        inventory.add_item(item)    
    except Exception as e:
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                             detail=str(e))
    
    return {"status": "Added item",
        "item_str": str(item)}

@inventory_router.get("/list-items") # tested
async def list_inventory(objects: bool = True):
    if inventory is None:
        raise HTTPException(status_code=err.HTTP_400_BAD_REQUEST, 
                             detail="Inventory not loaded")
    if objects:
        return {"items": tuple([str(item) for item in inventory.food_objs])}
    else:
        return {"items": inventory.foods.to_dict()}

# Searching items

# Deleting items
########################################################################
#                                 Saving                               #
########################################################################

@inventory_router.put("/save") # tested
async def save_inventory(name: str | None = None):
    if name:
        filename = f"{CURR_DIR}/inventories/{name}.csv"
    else:
        filename = f"{CURR_DIR}/inventories/{inventory.name}.csv"
    inventory.save(filename)

    return {"status": "Saved",
        "filename": filename}

    



