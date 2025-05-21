import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # To get KitchenInventory

import KitchenInventory as kit
from pprint import pprint


if __name__ == "__main__":
    pprint(kit.foods())
    print()
    pprint(kit.Food.Protein.GROUND_BEEF)