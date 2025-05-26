from __future__ import annotations
import logging
# from .logger_config import setup_logger
from pint import Quantity
from .category_database import foods, food_density_LUT, tools
from .pint_helpers import is_volume, is_density, is_mass

logger = logging.getLogger(__name__)

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
        self.ingredients: list[tuple[str, Quantity | int, Quantity]] = []
        self.tools: list[str] = []
        self.steps: list[str] = []

    @staticmethod
    def from_ingredients(name: str, ingredients: list[tuple[str, Quantity | int, Quantity | None]]):
        recipe = Recipe(name)
        for i in ingredients:
            recipe.add_ingredient(*i)
        return recipe
        
    def __str__(self):
        result = f"-----Recipe '{self.name}'-----" + "\n"

        if len(self.ingredients) > 0:
            result += "Ingredients:" + "\n"
            for tup in self.ingredients:
                result += f"  - {tup[0]} - {tup[1]}" + "\n"

        if len(self.tools) > 0:
            result += "Tools:" + "\n"
            for tool in self.tools:
                result += f"  - {tool}" + "\n"

        if len(self.steps) > 0:
            result += "Steps:" + "\n"
            for i, step in enumerate(self.steps):
                result += f"  {i+1}. {step}" + "\n"

        return result

    def add_ingredient(self, food_type: str, amount: Quantity | int | float, density: Quantity = None):
        """" Add mass or volume based on the Quantity type"""
        print(food_type)
        if food_type not in foods():
            raise ValueError(f"'Recipe {self.name}': Adding {amount} of '{food_type}' but food_type not in foods")

        if type(amount) is Quantity:
            self.__add_quantity_type(food_type, amount, density)
        elif type(amount) is int or type(amount) is float:
            self.__add_amount(food_type, amount)
        else:
            raise ValueError(f"'Recipe {self.name}': Adding {amount} of '{food_type}' but type not 'int', 'float', or 'Quantity'")
        
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
            raise ValueError(f"'Recipe {self.name}': Adding {amount} of '{food_type}' but units not mass or volume: was '{amount.dimensionality}'")

        
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
            self.ingredients.append((food_type, amount))
            return
    
        #Else tries density and adds
        if not is_density(density): 
            raise ValueError(f"Recipe '{self.name}': 'amount' must be in units of density but was '{density.dimensionality}'")
        
        self.ingredients.append((food_type, amount, density))

    def __add_amount(self, food_type: str, amount: float):

        if amount < 1:
            raise ValueError(f"Recipe '{self.name}': amount must be 1 or greater. was '{amount}'")
        
        self.ingredients.append((food_type, amount))

    def get_ingredients(self, servings: float = 1):
        new_ingredients: list[tuple[str, Quantity | int, Quantity]] = []
        for i in self.ingredients:
            food = list(i)
            food[1] *= servings
            new_ingredients.append(tuple(food))

        return new_ingredients
    
    def add_tool(self, tool_type: str):
        """" Add mass or volume based on the Quantity type"""

        if type(tool_type) is not str:
            raise ValueError(f"Recipe '{self.name}': Tool must be a string but was '{type(tool_type)}'")
        
        if tool_type not in tools():
            raise ValueError(f"'Recipe {self.name}': Adding '{tool_type}' not in foods")

        self.tools.append(tool_type)
    
    def add_steps(self, step: str):
        if type(step) is not str:
            raise ValueError(f"Recipe '{self.name}': Step must be a string but was '{type(step)}'")
        self.steps.append(step)

