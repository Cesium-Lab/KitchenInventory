import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit

# import argparse
# import asyncio
# import logging

# import uvicorn
# import fastapi
# import pydantic

from fastapi import FastAPI

app = FastAPI()

CURR_DIR = os.getcwd()

@app.get("/")
async def root():
    return {"message": "Welcome to The server!"}

@app.get("/foods")
async def get_foods():
    return {
        "foods": kit.foods()
    }



@app.get("/inventories")
async def get_inventory_numbers():
    directories = os.listdir(f"{CURR_DIR}/inventories")
    strings = [(i,directory) for i,directory in enumerate(directories)]
    return {
        "directories": strings
    }

# @app.get("/inventories/{id}")
# async def get_inventory(id: str):

    



