from KitchenInventory.logger_config import setup_logging, load_yaml
import logging
import os

import KitchenInventory as kit
from pint import Quantity

# Setting up logging
yamlfile = load_yaml("./config.yaml")
config = setup_logging(yamlfile)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    items: list[kit.Item | kit.CountableItem] = [
        kit.Item("Heavy milk", mass=Quantity(5, "lb"), density=Quantity(5, "g / mL")),
        kit.Item("Milk", volume=Quantity(5, "liter")),
        kit.CountableItem("egg.", 12)
    ]

    inventory = kit.Inventory("The Pit")
    # inventory = kit.Inventory.load("./inventories/The Pit.csv")

    inventory.add_items(items)
    inventory.foods["density (g/mL)"].iloc[1] = float(inventory.foods["density (g/mL)"].iloc[1]) * 9
    # print(inventory.foods.iloc[1]["density (g/mL)"])

    print(inventory.foods)

    inventory.save()

    # inventory_b = kit.Inventory.load("The PIT B", "./wow")

    # print(inventory_b.foods)

  