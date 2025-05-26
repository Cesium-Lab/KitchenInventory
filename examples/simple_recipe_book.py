import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit
from pint import Quantity

if __name__ == "__main__":

    book = kit.RecipeBook("The Pit")

    pancake_recipe = kit.Recipe("Pancakes?", "breakfast")
    pancake_recipe.add_ingredient(kit.Food.Dairy.MILK, Quantity(50, "mL"))
    pancake_recipe.add_ingredient(kit.Food.Grain.FLOUR, Quantity(2, "cup"))
    pancake_recipe.add_tool(kit.Tool.POT)
    pancake_recipe.add_step("Add flour to milk in a bowl")
    pancake_recipe.add_step("Mix until lumps gone")
    pancake_recipe.add_step("Cook until golden brown!")

    tiramisu_recipe = kit.Recipe("Tiramisu", "dessert")
    tiramisu_recipe.add_ingredient(kit.Food.Dairy.MILK, Quantity(50, "mL"))
    tiramisu_recipe.add_ingredient(kit.Food.Drink.Caffeine.COFFEE, Quantity(6, "tbsp"))
    tiramisu_recipe.add_ingredient(kit.Food.Bread.BASE, 1)
    tiramisu_recipe.add_tool(kit.Tool.PAN)
    tiramisu_recipe.add_step("Add ingredients to bowl")
    tiramisu_recipe.add_step("Mix until it looks ready")
    tiramisu_recipe.add_step("don't cook it")

    book.add_recipe(pancake_recipe)
    book.add_recipe(tiramisu_recipe)

    book.save(f"{sys.path[0]}/book.yaml")

    book2 = kit.RecipeBook.load(f"{sys.path[0]}/book.yaml")

    result = book2.recipes_by_name("Pancake")

    print(result[0])

    result = book2.recipes_by_name("Tiramisu")

    print(result[0])

    


