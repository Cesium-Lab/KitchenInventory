from __future__ import annotations
import pandas as pd
from pint import Quantity
from .Items import Item, CountableItem
import logging

logger = logging.getLogger(__name__)

class Inventory:

    columns = ["Name", "Food Type", "Mass (g)", "Volume (mL)", "Density (g/mL)", "Amount", "Expiration"]
    details_columns = ["Brand"]

    def __init__(self, name: str):
        self.name = name
        self.foods = pd.DataFrame(columns=Inventory.columns)
        self.food_objs = []


    def add_item(self, item: Item | CountableItem):
        row = {key:"" for key in Inventory.columns + Inventory.details_columns}
        row["Name"] = [item.name]
        row["Food Type"] = item.food_type
        row["Amount"] = 1
        row["Expiration"] = item.expiration.strftime("%Y-%m-%d") if item.expiration else ""

        def s(qty):
            return str(qty).strip(" dimensionless")

        if isinstance(item, Item):
            row["Mass (g)"] = [s(item.mass / Quantity(1, "g"))]
            row["Volume (mL)"] = [s(item.volume / Quantity(1, "mL"))]
            row["Density (g/mL)"] = [s(item.density / Quantity(1, "g/mL"))]

        if isinstance(item, CountableItem):
            row["Amount"] = [s(item.quantity)]

        if item.details:
            for column in Inventory.details_columns:
                if val := item.details.get(column.lower()):
                    row[column] = val

        row_df = pd.DataFrame.from_dict(row)

        self.foods = pd.concat([self.foods, row_df], ignore_index=True)

        # Logging
        stripped_row = {k: v for k, v in row.items() if v}
        logger.info(f"Added to {self.name}: {stripped_row}")

    def add_items(self, items: list[Item | CountableItem]):
        for item in items:
            self.add_item(item)
    
    @staticmethod
    def row_to_item(row: pd.Series):
        expiration = None if row.get("Expiration") == "" else row["Expiration"]

        if row["Mass (g)"] and row["Volume (mL)"]:
            return Item(
                name = row["Name"],
                food_type = row["Food Type"],
                mass = Quantity(float(row["Mass (g)"]), 'g'),
                density = Quantity(float(row["Density (g/mL)"]), 'g/mL'),
                expiration = expiration
            )
        
        return CountableItem(
                name = row["Name"],
                food_type = row["Food Type"],
                quantity = row["Amount"],
                expiration = expiration
            )

    # def get_food_rows(self, name: str):
    #     rows = self.foods[self.foods['Name'] == name]
    #     return rows
    
    def foods_by_name(self, name: str) -> list[Item | CountableItem]:
        rows = self.foods[self.foods["Name"] == name]
        return [Inventory.row_to_item(row) for _,row in rows.iterrows()]
    
    def foods_by_type(self, food_type: str) -> list[Item | CountableItem]:
        rows = self.foods[self.foods["Food Type"].str.contains(food_type)]
        return [Inventory.row_to_item(row) for _,row in rows.iterrows()]

    def reset(self):
        self.foods = self.foods[0:0]

    def save(self, filename: str = None):
        if filename is None:
            filename = f"./inventories/{self.name}.csv"
        
        with open(filename, 'w') as f:
            f.write(self.foods.to_csv(index=False))
        logger.info(f"Saved {len(self.foods)} foods into '{filename}': {self}")

    @classmethod
    def load(self, filename: str, name: str = None) -> Inventory:
        if name is None:
            name = filename.split("/")[-1].split(".")[0]
        inv = Inventory(name)
        with open(filename, 'r') as f:
            inv.foods = pd.read_csv(f).fillna('')
            inv.food_objs = [Inventory.row_to_item(row) for _,row in inv.foods.iterrows()]

        logger.info(f"Loaded {len(inv.foods)} foods from '{filename}' into '{inv.name}': {inv}")


        return inv

        


