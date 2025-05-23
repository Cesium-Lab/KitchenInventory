from __future__ import annotations
import logging
# from .logger_config import setup_logger
from pint import Quantity
from .foods import foods
from datetime import datetime, timedelta
import numpy as np
# from .Locations.the_pit import Location

# https://en.wikipedia.org/wiki/Centimetre%E2%80%93gram%E2%80%93second_system_of_units
# g, mL 

logger = logging.getLogger(__name__)

class Item:
    """Tracks items using the mass and density as a \"canonical\" amount"""
    def __init__(self, name: str, food_type: str, *, mass: Quantity = None, volume: Quantity = None, density: Quantity = None, expiration: str = None, **kwargs) -> Item:
        self.name = name
        self.expiration = datetime.strptime(expiration, "%Y-%m-%d") if expiration else None
        self.details = kwargs
        
        if food_type not in foods():
            raise ValueError(f"Food type '{food_type}' must be in foods list")
        
        self.food_type = food_type
        # Mass defined
        if mass:

            self._mass = mass.to("g")
            if volume: # mass and volume
                # self._volume = volume
                self._density: Quantity = Quantity(mass / volume) # Stupid type checking thing
            elif density: # mass and density
                self._density = density.to("g/mL")
                # self._volume: Quantity = Quantity(mass * density) # Stupid type checking thing
            else: # mass
                logger.info(f"Setting density of \"{self.name}\" to 1 g/mL automatically")
                self._density = Quantity(1, "g/mL")
                # self._volume: Quantity = Quantity(mass * density) # Stupid type checking thing

        # Mass defined
        elif volume:
            volume = volume.to("mL")
            # self._volume = volume
            if density: # volume and density
                self._density = density.to("g/mL")
                self._mass: Quantity = Quantity(volume * density) # Stupid type checking thing
            else: # volume
                logger.info(f"Setting density of \"{self.name}\" to 1 g/mL automatically")
                self._density = Quantity(1, "g/mL")
                self._mass: Quantity = Quantity(volume * self._density) # Stupid type checking thing
                # self._volume: Quantity = Quantity(mass * density) # Stupid type checking thing
            
        else:
            raise ValueError("If density is provided, must provide mass or volume")
        
    def __str__(self):
        return f"[\"{self.name}\" - {self.food_type}: ({self.mass}, {self.volume}, {self._density})]"


    # Mass 
    @property
    def mass(self):
        return self._mass
    
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
        return self._density
    
    @density.setter
    def density(self, _):
        raise NotImplementedError("Should not be resetting density after initialization")
    
    @property
    def days_left(self) -> int | None:
        if self.expiration is None:
            return np.inf
        diff: timedelta = self.expiration - datetime.today()
        return diff.days

class CountableItem:
    """Tracks countable items using the mass as a \"canonical\" amount"""
    def __init__(self, name: str, food_type: str, quantity: int, expiration: str = None, **kwargs) -> CountableItem:
        self.name = name
        self.expiration = datetime.strptime(expiration, "%Y-%m-%d") if expiration else None
        self.food_type = food_type
        self.details = kwargs
        self.quantity = quantity

    def __str__(self):
        return f"[\"{self.name}\" - {self.food_type}: {self.quantity} count]"
    
    @property
    def days_left(self) -> int | None:
        if self.expiration is None:
            return np.inf
        diff: timedelta = self.expiration - datetime.today()
        return diff.days
    
