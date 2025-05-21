from __future__ import annotations
import pandas as pd
from pint import Quantity
from .Items import Item, CountableItem

import logging

logger = logging.getLogger(__name__)

class Inventory:

    columns = ["Name", "mass (g)", "volume (mL)", "density (g/mL)", "amount"]

    def __init__(self, name: str):
        self.name = name
        self.foods = pd.DataFrame(columns=Inventory.columns)


    def add_item(self, item: Item | CountableItem):
        row = {key:"" for key in Inventory.columns}
        row["Name"] = [item.name]
        row["amount"] = 0

        def s(qty):
            return str(qty).strip(" dimensionless")

        if isinstance(item, Item):
            row["mass (g)"] = [s(item.mass / Quantity(1, "g"))]
            row["volume (mL)"] = [s(item.volume / Quantity(1, "mL"))]
            row["density (g/mL)"] = [s(item.density / Quantity(1, "g/mL"))]

        if isinstance(item, CountableItem):
            row["amount"] = [s(item.quantity)]

        if item.details:
            row["Expiration"] = [item.details["Expiration"]]

        row_df = pd.DataFrame.from_dict(row)

        self.foods = pd.concat([self.foods, row_df], ignore_index=True)

        # Logging
        stripped_row = {k: v for k, v in row.items() if v}
        logger.info(f"Added {stripped_row} to {self.name}")

    def add_items(self, items: list[Item | CountableItem]):
        for item in items:
            self.add_item(item)

    def reset(self):
        self.foods = self.foods[0:0]

    def save(self, filename: str = None):
        if filename is None:
            filename = f"./inventories/{self.name}.csv"
        
        with open(filename, 'w') as f:
            f.write(self.foods.to_csv(index=False))


    @classmethod
    def load(self, filename: str, name: str = None) -> Inventory:
        if name is None:
            name = filename.split("/")[-1].split(".")[0]
        inv = Inventory(name)
        with open(filename, 'r') as f:
            inv.foods = pd.read_csv(f).fillna('')

        return inv

        


