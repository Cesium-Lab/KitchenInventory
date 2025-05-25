import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit
from pint import Quantity

if __name__ == "__main__":

    inventory = kit.Inventory("The Pit")
    recipe = kit.Recipe("Pancakes?")
    print(recipe)
    recipe.add_ingredient(kit.Food.Dairy.MILK, Quantity(50, "mL"))
    recipe.add_ingredient(kit.Food.Grain.FLOUR, Quantity(2, "cup"))
    print(recipe)
    recipe.add_tool(kit.Tool.POT)
    print(recipe)
    recipe.add_steps("Add flour to milk in a bowl")
    recipe.add_steps("Mix until lumps gone")
    recipe.add_steps("Cook until golden brown!")
    print(recipe)

