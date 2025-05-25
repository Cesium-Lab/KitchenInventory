import logging
import KitchenInventory as kit
from pint import Quantity
# from datetime import datetime
# import sys
# Setting up logging
yamlfile = kit.load_yaml("./config.yaml")
config = kit.setup_logging(yamlfile)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    items: list[kit.Item | kit.CountableItem] = [
        kit.Item(
            "Heavy milk",
            kit.Food.Dairy.MILK,
            mass=Quantity(5, "lb"),
            density=Quantity(5, "g / mL"),
            expiration="2025-05-30",
            brand="Heavy milk Corporation"
            ),
        kit.Item(
            "Milk", 
            kit.Food.Dairy.MILK,
            volume=Quantity(5, "liter"),
            expiration="1025-05-30"),
        kit.CountableItem(
            "egg.", 
            kit.Food.Dairy.EGG,
            12,
            brand="Eggs-R-Us"),
    ]

    # item = kit.Item('7', '/bread', mass=Quantity(5, 'kg'), volume=None, density=None, expiration="")


    inventory = kit.Inventory("The Pit")
    recipe = kit.Recipe("recipe")
    print(items[0].mass.u)

    # recipe.add_ingredient_by_mass("/bread", Quantity(5, "g"))
    # recipe.add_ingredient_by_quantity("/egg", 12)


    # inventory = kit.Inventory.load("./inventories/The Pit.csv")

    # inventory.add_item(item)
    # inventory.add_items(items)

    # print(inventory.foods)




    # inventory.save()
    # inventory_b = kit.Inventory.load("./inventories/The Pit.csv")
    # inventory_b.save()
    # inventory_c = kit.Inventory.load("./inventories/The Pit.csv")

    # dairy_rows = inventory_c.foods_by_type(kit.Food.Dairy.BASE)
    # milk_rows = inventory_c.foods_by_type("Milk")
    
    # for row in dairy_rows:
    #     print(row)

    # print(kit.Food.Dairy.Cheese.CHEESE_STICK)
    # print(kit.foods())

    


  