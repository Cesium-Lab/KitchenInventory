from __future__ import annotations
import logging
# from .logger_config import setup_logger
from pint import Quantity
from .category_database import foods
from datetime import datetime, timedelta
import numpy as np
# from .Locations.the_pit import Location

# https://en.wikipedia.org/wiki/Centimetre%E2%80%93gram%E2%80%93second_system_of_units
# g, mL 

logger = logging.getLogger(__name__)

class Item:
    """Tracks items using the mass and density as a \"canonical\" amount
    
    Can be defined by 
    - mass
    - mass, density
    - volume
    - volume, density
    - mass, volume

    

    Cannot be defined by just density
    
    
    """
    def __init__(self, name: str, food_type: str, *, mass: Quantity = None, volume: Quantity = None, density: Quantity = None, expiration: str = None, **kwargs) -> Item:
        self.name = name
        self.expiration = datetime.strptime(expiration, "%Y-%m-%d") if expiration else None
        if self.days_left < 0:
            logger.error(f"Item '{self.name}' created with expiration date in past")
        
        self.details = kwargs
        
        if food_type not in foods():
            raise ValueError(f"Food type '{food_type}' must be in foods list")
        self.food_type = food_type

        self.__define_properties(mass, volume, density)
        
    def __define_properties(self, mass: Quantity, volume: Quantity, density: Quantity):

        # Mass defined
        if mass:
            if type(mass) is not Quantity:
                raise ValueError(f"Mass must be of type {Quantity} and not {type(mass)}")
            self._mass = mass

            if volume: # Mass and Volume
                if type(volume) is not Quantity:
                    raise ValueError(f"Volume must be of type {Quantity} and not {type(volume)}")
                self._density: Quantity = Quantity(mass / volume) # Stupid type checking thing
            elif density: # mass and density
                if type(density) is not Quantity:
                    raise ValueError(f"Density must be of type {Quantity} and not {type(density)}")
                self._density = density
            else: # mass
                logger.info(f"Setting density of '{self.name}' to '1 g/mL' automatically")
                self._density = Quantity(1, "g/mL")

        # Mass defined
        elif volume:
            if type(volume) is not Quantity:
                raise ValueError(f"Volume must be of type {Quantity} and not {type(volume)}")
            volume = volume
            # self._volume = volume
            if density: # volume and density
                self._density = density
                self._mass: Quantity = Quantity(volume * density) # Stupid type checking thing
            else: # volume
                logger.info(f"Setting density of '{self.name}' to '1 g/mL' automatically")
                self._density = Quantity(1, "g/mL")
                self._mass: Quantity = Quantity(volume * self._density) # Stupid type checking thing
            
        else:
            raise ValueError("If density is provided, must provide mass or volume")
    def __str__(self):
        return f"['{self.name}' - {self.food_type}: ({self.mass}, {self.volume}, {self._density})]"


    # Mass 
    @property
    def mass(self):
        return self._mass.to("g")
    
    @mass.setter
    def mass(self, new_mass: Quantity):
        self._mass = new_mass

    # Volume 
    @property
    def volume(self):
        return (self._mass / self._density).to("mL")
    
    @volume.setter
    def volume(self, new_vol: Quantity):
        self._mass = (new_vol * self._density)

    # Density 
    @property
    def density(self):
        return self._density.to("g/mL")
    
    @density.setter
    def density(self, _):
        raise PermissionError("Should not be resetting density after initialization")
    
    @property
    def days_left(self) -> int | float:
        if self.expiration is None:
            return np.inf
        diff: timedelta = self.expiration.date() - datetime.today().date()
        return diff.days
    


class CountableItem:
    """Tracks countable items using the mass as a \"canonical\" amount"""
    def __init__(self, name: str, food_type: str, quantity: int | float, expiration: str = None, **kwargs) -> CountableItem:
        self.name = name
        self.expiration = datetime.strptime(expiration, "%Y-%m-%d") if expiration else None
        if self.days_left < 0:
            logger.error(f"CountableItem '{self.name}' created with expiration date in past")
        
        if food_type not in foods():
            raise ValueError(f"Food type '{food_type}' must be in foods list")
        self.food_type = food_type
        
        if (type(quantity) is not int and type(quantity) is not float) or quantity < 0:
            raise ValueError(f"Quantity must be int or float, and 0 or greater. Input was '{quantity}' with type '{type(quantity)}'")

        self.quantity = quantity

        self.details = kwargs

    def __str__(self):
        return f"['{self.name}' - {self.food_type}: {self.quantity} count]"
    
    @property
    def days_left(self) -> int | None:
        if self.expiration is None:
            return np.inf
        diff: timedelta = self.expiration.date() - datetime.today().date()
        return diff.days
    
class KitchenTool:

    def __init__(self, name: str, tool_type: str):
        self.name = name
        self.tool_type = tool_type
