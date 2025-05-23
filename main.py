import logging
import KitchenInventory as kit
from pint import Quantity
import os

yamlfile = kit.load_yaml("./config.yaml")
config = kit.setup_logging(yamlfile)
logger = logging.getLogger(__name__)

def make_qty(s: str):
    if type(s) is not str or len(s) == 0:
        return None
    num = s.split()[0]
    unit = "".join(s.split()[1:])
    # print(s)
    # print(num)
    # print(unit)
    return Quantity(float(num), unit)

def add_food(inv: kit.Inventory):
    mass = None
    expiration = None
    food_type = None

    # Inputs
    name = input("Name of food\n--> ")
    food_type = input("What type of food? (Food type specifiers start with a '/' like '/drink/alcohol')\n--> ")
    expiration = input("In YYYY-MM-DD format, expiration (blank for no expiration)")

    volume = None
    density = None

    
    mass = input("Mass of food (leave blank for volume-defined or amount-defined)\n--> ")
    print(type(mass))
    if mass == "":
        volume = input("Volume of food (leave blank for amount-defined)\n--> ")
        density = input("Density of food (leave blank if basically water)\n--> ")

    else:
        density = input("Density of food (leave blank if mass-defined or amount-defined)\n--> ")

    if not mass and not volume and not density:
        amount = int(input("Quantity of items\n--> "))
        item = kit.CountableItem(name, food_type, amount, expiration=expiration)
    else:
        item = kit.Item(name, food_type, mass=make_qty(mass), volume=make_qty(volume), density=make_qty(density), expiration=expiration)
    inv.add_item(item)

if __name__ == "__main__":
    os.system("clear")
    print("\nWelcome to Kitchen Inventory Tracker frontend!!!!1!1!!!!!1!!!1!!")
    
    inventories = os.listdir("./inventories")


    if len(inventories) > 0:
        print(f"\tFound {len(inventories)} inventories:")
        for i, inv in enumerate(inventories):
            print(f"\t{i+1}. {inv}")

        num = int(input("Which inventory to open?\n"))
        if num <= 0 or num > len(inventories):
            raise ValueError(f"Valid numbers are 1 through {len(inventories)}")

        inventory = kit.Inventory.load(f"./inventories/{inventories[num-1]}")
    else:
        choice = input("Zero inventories detected, would you like to create a new one (c) or quit (anything else)\n")
        if choice != 'c':
            print("Goodbye!")
            exit()
        name = input("Input name:\n")
        inventory = kit.Inventory(name=name)

    

    choice = ""
    
    def choose_what_to_do():
        os.system("clear")
        print()
        print(inventory.foods)
        print()
        
        print("What do you want to do?")
        print("1. Add items in workspace.py")
        print("2. Find items by attribute") # Lists attributes and finds items
        print("3. Find items by food type") # Food type
        print("4. Add custom food")
        print("...")
        print("q. Save and exit") # Lists attributes and finds items

        return input()
    
    choice = choose_what_to_do()
    invalid_counter = 0

    while choice != 'q':


        match choice:
            case '1': # Add items in workspace.py
                print(f"Chose {choice}")
            case '2': # Find by attribute
                print(f"Chose {choice}")
            case '3': # Find by food type
                food_type = input("What type of food? (Food type specifiers start with a '/' like '/drink/alcohol')\n")
                for row in inventory.foods_by_type(food_type):
                    print(row)
                print()
            case '4':
                add_food(inventory)
            case _:
                invalid_counter += 1
                print("Invalid choice\n")

        choice = choose_what_to_do()

    inventory.save()
    print("Saved!")


    print("Goodbye!")
            

  