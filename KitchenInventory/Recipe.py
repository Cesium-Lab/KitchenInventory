from __future__ import annotations
import logging
# from .logger_config import setup_logger
from pint import Quantity
from .foods import foods, food_density_LUT
from datetime import datetime, timedelta
import numpy as np
from .Items import Item, CountableItem
# from .Locations.the_pit import Location

# https://en.wikipedia.org/wiki/Centimetre%E2%80%93gram%E2%80%93second_system_of_units
# g, mL 

logger = logging.getLogger(__name__)

def is_mass(x: Quantity):
    return x.dimensionality == "[mass]"

def is_volume(x: Quantity):
    return x.dimensionality == "[length] ** 3"

def is_density(x: Quantity):
    return x.dimensionality == "[mass] / [length] ** 3"

class Recipe:
    """ 
    - List of ingredients
    - List of tools
    - Serving Size
    - Nutrition facts (if any)

    - Description
    - List of steps


    """

    def __init__(self, name: str):
        self.name = name
        self.ingredients: list[tuple[str, Quantity | int, Quantity | None]] = []
        
    def __str__(self):
        result = f"---Recipe '{self.name}'---" + "\n"
        result += "Ingredients:" + "\n"
        for i in self.ingredients:
            result += f"- {i[0]} - {i[1]}" + "\n"
        return result
    

    def add_ingredient(self, food_type: str, amount: Quantity | int, density: Quantity = None):
        """" Add mass or volume based on the Quantity type"""

        if food_type not in foods():
            raise ValueError(f"'Recipe {self.name}': Adding {amount} of '{food_type}' but food_type not in foods")

        if type(amount) is Quantity:
            self.__add_quantity_type(food_type, amount, density)
        elif type(amount) is int:
            self.__add_int(food_type, amount)
        else:
            raise ValueError(f"'Recipe {self.name}': Adding {amount} of '{food_type}' but type not 'int' or 'Quantity'")
        
        logger.info(f"Recipe '{self.name}': Added {amount} of '{food_type}'")

    def __add_quantity_type(self, food_type: str, amount: Quantity, density: Quantity = None):
        """ Add Quantity type """

        if amount.m <= 0.0:
            raise ValueError(f"'amount' must be greater than 0 but was {amount.m}")

        if is_mass(amount):
            self.ingredients.append((food_type, amount))
        elif is_volume(amount):
            self.__add_volume(food_type, amount, density)
        else:
            print("BRUH")

        
    def __add_volume(self, food_type: str, amount: Quantity, density: Quantity = None):
        # Tries LUT and adds
        if food_type in food_density_LUT.keys():
            tup = food_density_LUT[food_type]
            density = Quantity(tup[0], tup[1])
            self.ingredients.append((food_type, amount, density))
            return
            
        # Defaulting to density
        logger.info(f"Recipe '{self.name}': '{food_type}' not found in 'food_density_LUT' defaulting to density parameter")

        # If no density added, do 1 g/mL
        if density is None:
            self.ingredients.append((food_type, amount, None))
            return

        #Else tries density and adds
        if not is_density(density): 
            raise ValueError(f"Recipe '{self.name}': 'amount' must be in units of density but was '{density.dimensionality}'")
        
        self.ingredients.append((food_type, amount, density))

        return

    def __add_int(self, food_type: str, amount: int):
        pass
