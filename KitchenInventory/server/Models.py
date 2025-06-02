from pydantic import BaseModel, Field, ValidationError, conint
from ..Items import Item
from ..Items import CountableItem
from pint import Quantity

ITEM_OK = "OK"

class ItemBase(BaseModel):
    # Required
    name: str
    food_type: str

    # Amount definitions
    mass: str | None = None
    volume: str | None = None
    density: str | None = None

    # Details
    expiration: str = None
    brand: str = None
    description: str = None
        
    def to_Item(self) -> Item:
        self.check_amounts()
        mass, volume, density = self.get_quantities()

        details = {}
        if self.brand:
            details["Brand"] = self.brand
        if self.description:
            details["Description"] = self.description
        
        item = Item(self.name, self.food_type,
                    mass=mass, volume=volume, density=density,
                    expiration=self.expiration,
                    details=details)
        
        return item

    def check_amounts(self):
        if self.mass is not None:
            tup = self.mass.split(" ",1)
            
            if len(tup) != 2:
                raise ValueError(f"Mass '{self.mass}' must contain the format '# unit'")
            
        if self.volume is not None:
            tup = self.volume.split(" ",1)
            
            if len(tup) != 2:
                raise ValueError(f"Volume '{self.volume}' must contain the format '# unit'")
            
        if self.density is not None:
            tup = self.density.split(" ",1)
            
            if len(tup) != 2:
                raise ValueError(f"Density '{self.density}' must contain the format '# unit'")
            
    def get_quantities(self):

        mass, volume, density = None, None, None
        if self.mass:
            split_str = self.mass.split(" ",1)
            # print(split_str[1])
            mass = Quantity(float(split_str[0]), split_str[1])

        if self.volume:
            split_str = self.volume.split(" ",1)
            # print(split_str[1])
            volume = Quantity(float(split_str[0]), split_str[1])

        if self.density:
            split_str = self.density.split(" ",1)
            # print(split_str[1])
            density = Quantity(float(split_str[0]), split_str[1])

        return mass, volume, density


        
        