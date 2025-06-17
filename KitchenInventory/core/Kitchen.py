from __future__ import annotations
import pandas as pd
from pint import Quantity
from .Items import Item, CountableItem
from .Recipe import Recipe
import logging
import yaml
from pprint import pprint
logger = logging.getLogger(__name__)


class Inventory:
    """ 
    - Makes a database of items
    - Can search items with common food
    """

    columns = ["Name", "Food Type", "Mass (g)", "Volume (mL)", "Density (g/mL)", "Amount", "Expiration"]
    details_columns = ["Brand", "Description"]

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
        

        if isinstance(item, Item):
            row["Mass (g)"] = [str(item.mass.m)]
            row["Volume (mL)"] = [str(item.volume.m)]
            row["Density (g/mL)"] = [str(item.density.m)]

        if isinstance(item, CountableItem):
            row["Amount"] = [str(item.quantity)]

        if item.details:
            for column in Inventory.details_columns:
                print(column)
                if val := item.details.get(column.lower()):
                    print(val)
                    row[column] = val

        row_df = pd.DataFrame.from_dict(row)

        self.foods = pd.concat([self.foods, row_df], ignore_index=True)

        # Logging
        stripped_row = {k: v for k, v in row.items() if v}
        self.food_objs.append(item)
        logger.info(f"Added to {self.name}: {stripped_row}")
        print(self.foods)

    def add_items(self, items: list[Item | CountableItem]):
        for item in items:
            self.add_item(item)

    # def use_item(self, item: Item)
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

    @staticmethod
    def load(filename: str, name: str = None) -> Inventory:
        if name is None:
            name = filename.split("/")[-1].split(".")[0]
        inv = Inventory(name)
        with open(filename, 'r') as f:
            inv.foods = pd.read_csv(f).fillna('')
            inv.food_objs = [Inventory.row_to_item(row) for _,row in inv.foods.iterrows()]

        logger.info(f"Loaded {len(inv.foods)} foods from '{filename}' into '{inv.name}': {inv}")

        return inv
    
    # def load(self, filename: str, name: str = None):
    #     if name is None:
    #         name = filename.split("/")[-1].split(".")[0]
    #     with open(filename, 'r') as f:
    #         self.foods = pd.read_csv(f).fillna('')
    #         self.food_objs = [Inventory.row_to_item(row) for _,row in self.foods.iterrows()]

    #     logger.info(f"Loaded {len(self.foods)} foods from '{filename}' into '{self.name}': {self}")
        
    
class RecipeBook:
    """ 
    - Makes and saves a yaml of recipes
    - Can search recipes
    """
    def __init__(self, name: str):
        self.name = name
        self.recipes: list[dict] = []
        self.recipe_objs: list[Recipe] = []

    def add_recipe(self, recipe: Recipe):
        if type(recipe) is not Recipe:
            raise ValueError(f"RecipeBook '{self.name}': recipe must be Recipe, not {type(recipe)}")

        recipe_dict = recipe.__dict__

        if recipe.ingredients != []:
            ingredients = []
            for i in recipe.ingredients:
                if type(i[1]) is Quantity:
                    row = [i[0], i[1].m, str(i[1].u)]
                    if len(i) == 3:
                        row += [i[2].m, str(i[2].u)]
                else:
                    row = [i[0], i[1]]
                ingredients.append(row)
            recipe_dict["ingredients"] = ingredients

            
        self.recipes.append(recipe_dict)

        logger.info(f"Added to {self.name}: {recipe_dict}")

    def add_recipes(self, recipes: list[Recipe]):
        for recipe in recipes:
            self.add_recipe(recipe)

    @staticmethod
    def value_to_recipe(value: dict) -> Recipe:
        if value.get("name") is None:
            raise ImportError("RecipeBook importing Recipe: Row did not contain 'name'")
        name = value["name"]

        recipe = Recipe(name)
        
        if value.get("ingredients") is not None:
            for i in value["ingredients"]:
                match len(i):
                    case 2:
                        row = i
                    case 3:
                        row = [i[0], Quantity(i[1], i[2])]
                    case 5:
                        row = [i[0], Quantity(i[1], i[2]), Quantity(i[3], i[4])]
                    case _:
                        raise ValueError(f"Ingredient '{i}' invalid length of '{len(i)}'")

                recipe.ingredients.append(row)

        if value.get("tools") is not None:
            recipe.tools = value["tools"]
        if value.get("steps") is not None:
            recipe.steps = value["steps"]

        return recipe

    def recipes_by_name(self, name: str):
        names = [recipe for recipe in self.recipes if name in recipe["name"]]
        return [RecipeBook.value_to_recipe(recipe) for recipe in names]

    def recipes_by_type(self, recipe_type: str):
        names = [recipe for recipe in self.recipes if recipe_type in recipe["recipe_type"]]
        return [RecipeBook.value_to_recipe(recipe) for recipe in names]

    def reset(self):
        self.recipes = []
        self.recipe_objs = []

    def save(self, filename: str = None):
        if filename is None:
            filename = f"./recipe_books/{self.name}.yaml"
        
        with open(filename, 'w') as f:
            yaml.safe_dump(self.recipes, f)
        logger.info(f"Saved {len(self.recipes)} recipes into '{filename}': {self}")

    
    @classmethod
    def load(self, filename: str, name: str = None):
        if name is None:
            name = filename.split("/")[-1].split(".")[0]
        book = RecipeBook(name)
        with open(filename, 'r') as f:
            book.recipes = yaml.safe_load(f)
            book.recipe_objs = [RecipeBook.value_to_recipe(row) for row in book.recipes]

        logger.info(f"Loaded {len(book.recipes)} foods from '{filename}' into '{book.name}': {book}")

        return book

    

    
        


