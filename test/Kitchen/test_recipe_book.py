import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../..")) # To get KitchenInventory
# sys.path.insert(1, os.getcwd()) # Assumes running in root

import KitchenInventory as kit
import pytest
from pint import Quantity

########################################################################
#                             RecipeBook                               #
########################################################################

class TestRecipeBook:
    
    def test_constructor(self):
        recipe_book = kit.RecipeBook("name")
        assert recipe_book.name == "name"
        assert recipe_book.recipes == []
        assert recipe_book.recipe_objs == []

    class TestAddRecipe:

        def test_add_non_recipe(self):
            book = kit.RecipeBook("name")
            with pytest.raises(ValueError) as e:
                book.add_recipe(5.0)
            assert "recipe must be Recipe, not" in str(e.value)


        def test_empty(self):
            name = "recipe"
            recipe = kit.Recipe(name)

            book = kit.RecipeBook("book")
            book.add_recipe(recipe)

        def test_ingredients(self):
            name = "recipe"

            ingredients = [
                [kit.Food.Dairy.MILK, 1, "cup", 1.03, "gram / milliliter"],
                [kit.Food.Spice.SALT, 1, "tablespoon"],
                [kit.Food.Meat.CHICKEN, 0.5, "pound"]
            ]

            recipe = kit.Recipe(name)
            recipe.add_ingredient(kit.Food.Dairy.MILK, Quantity(1, "cup"))
            recipe.add_ingredient(kit.Food.Spice.SALT, Quantity(1, "tbsp"))
            recipe.add_ingredient(kit.Food.Meat.CHICKEN, Quantity(0.5, "pound"))

            book = kit.RecipeBook("book")
            book.add_recipe(recipe)

            assert len(book.recipes) == 1
            result = book.recipes[0]

            assert result["name"] == "recipe"
            assert result["ingredients"] == ingredients 
            assert result["steps"] == []
            assert result["tools"] == []

        def test_steps_and_tools(self):
            name = "recipe"

            recipe = kit.Recipe(name)
            recipe.add_step("Step 1")
            recipe.add_tool("knife")

            book = kit.RecipeBook("book")
            book.add_recipe(recipe)
            

            assert len(book.recipes) == 1
            result = book.recipes[0]

            assert result["name"] == "recipe"
            assert result["ingredients"] == []
            assert result["steps"] == ["Step 1"]
            assert result["tools"] == ["knife"]

    class TestValueToItem:

        def test_full_pancake(self):
            pancake_dict = {}
            pancake_dict["name"] = "pancake"
            pancake_dict["ingredients"] = [
                ["dairy-milk", 50, "mL", 1.03, "g/mL"],
                ["grain-flour", 2, "cup"]
            ]
            pancake_dict["steps"] = [
                "Step 1",
                "Step 2",
                "Step 3",
                "Step 4",
                "Step 5"
            ]
            pancake_dict["tools"] = ["pot"]

            recipe: kit.Recipe = kit.RecipeBook.value_to_recipe(pancake_dict)

            assert recipe.name == "pancake"
            assert recipe.ingredients == [
                ["dairy-milk", Quantity(50, "mL"), Quantity(1.03, "g/mL")],
                ["grain-flour", Quantity(2, "cup")]
            ]
            assert recipe.steps == [
                "Step 1",
                "Step 2",
                "Step 3",
                "Step 4",
                "Step 5"
            ]
            assert recipe.tools == ["pot"]

        def test_empty(self):
            pancake_dict = {}
            pancake_dict["name"] = "pancake"

            recipe: kit.Recipe = kit.RecipeBook.value_to_recipe(pancake_dict)

            assert recipe.name == "pancake"
            assert recipe.ingredients == []
            assert recipe.steps == []
            assert recipe.tools == []

    class TestFindByName:

        def test_find_by_name(self):
            book = kit.RecipeBook("book")
            book.add_recipe(kit.Recipe("cool"))
            book.add_recipe(kit.Recipe("cool2"))
            book.add_recipe(kit.Recipe("other"))
            book.add_recipe(kit.Recipe("other2"))

            result = book.recipes_by_name("cool")
            assert len(result) == 2
            assert [r.name for r in result] == ["cool", "cool2"]

            result = book.recipes_by_name("other")
            assert len(result) == 2
            assert [r.name for r in result] == ["other", "other2"]

            result = book.recipes_by_name("2")
            assert len(result) == 2
            assert [r.name for r in result] == ["cool2", "other2"]

    class TestFindByType:

        def test_find_by_name(self):
            book = kit.RecipeBook("book")
            book.add_recipe(kit.Recipe("cool", "type"))
            book.add_recipe(kit.Recipe("cool2", "type1"))
            book.add_recipe(kit.Recipe("other", "haha"))
            book.add_recipe(kit.Recipe("other2", "haha1"))

            result = book.recipes_by_type("type")
            assert len(result) == 2
            assert [r.name for r in result] == ["cool", "cool2"]

            result = book.recipes_by_type("haha")
            assert len(result) == 2
            assert [r.name for r in result] == ["other", "other2"]

            result = book.recipes_by_type("1")
            assert len(result) == 2
            assert [r.name for r in result] == ["cool2", "other2"]

    class TestReset:

        def test_reset(self):
            book = kit.RecipeBook("book")
            book.add_recipe(kit.Recipe("cool"))
            book.add_recipe(kit.Recipe("cool2"))
            book.add_recipe(kit.Recipe("other"))
            book.add_recipe(kit.Recipe("other2"))

            book.reset()
            assert len(book.recipes) == 0
            assert len(book.recipe_objs) == 0



            

