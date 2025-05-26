import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit
from pint import Quantity

if __name__ == "__main__":

    recipe = kit.Recipe("Pancakes?")
    recipe.add_ingredient(kit.Food.Dairy.MILK, Quantity(50, "mL"))
    recipe.add_ingredient(kit.Food.Grain.FLOUR, Quantity(2, "cup"))
    recipe.add_tool(kit.Tool.POT)
    recipe.add_step("Add flour to milk in a bowl")
    recipe.add_step("Mix until lumps gone")
    recipe.add_step("Cook until golden brown!")
    
    print(recipe)

