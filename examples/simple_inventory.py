import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit
from pint import Quantity

if __name__ == "__main__":

    items: list[kit.Item | kit.CountableItem] = [
        kit.Item("Heavy milk", mass=Quantity(5, "lb"), density=Quantity(5, "g / mL")),
        kit.Item("Milk", volume=Quantity(5, "liter")),
        kit.CountableItem("egg.", 12)
    ]

    inventory = kit.Inventory("The Pit")

    inventory.add_items(items)
    
    print(inventory.foods)

    inventory.save(f"{sys.path[0]}/The Pit.csv")

    inventory_b = kit.Inventory.load(f"{sys.path[0]}/The Pit.csv", "The PIT B")

    egg_rows = inventory_b.get_foods("egg.")
    milk_rows = inventory_b.get_foods("Milk")
    
    for row in egg_rows + milk_rows:
        print(row)

  


  