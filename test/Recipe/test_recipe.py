import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../..")) # To get KitchenInventory

import KitchenInventory as kit
import pytest
from pint import Quantity
# from pprint import pprint

########################################################################
#                                  Recipe                              #
########################################################################

class TestRecipe:

    class TestInitilization:
        def test_constructor(self):

            recipe = kit.Recipe("name")

            assert recipe.name == "name"
            assert recipe.ingredients == []
            assert recipe.tools == []
            assert recipe.steps == []

        def test_from_ingredients_good(self):
            ingredients = [
                [kit.Food.Dairy.MILK, Quantity(1, "cup"), Quantity(1.03, "g/mL")],
                [kit.Food.Spice.SALT, Quantity(1, "tbsp")],
                [kit.Food.Meat.CHICKEN, Quantity(0.5, "pound")]
            ]

            recipe = kit.Recipe.from_ingredients("name", ingredients)

            assert len(recipe.ingredients) == 3
            for expected, actual in zip(ingredients, recipe.ingredients):
                assert expected == actual

        def test_from_ingredients_bad(self):
            ingredients = [
                (kit.Food.Dairy.MILK, Quantity(1, "m"))
            ]

            with pytest.raises(ValueError) as e:
                kit.Recipe.from_ingredients("name", ingredients)
            assert "units not mass or volume" in str(e.value)

    class TestAddIngredient:

        def test_bad_food_type(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError) as e:
                recipe.add_ingredient("name", 1)
            assert "food_type not in foods" in str(e.value)

        def test_bad_type(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, True)
            assert "type not 'int', 'float', or 'Quantity'" in str(e.value)

        def test_0_or_less(self):
            recipe = kit.Recipe("name")
            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, Quantity(0, 'g'))
            assert "must be greater than 0" in str(e.value)
            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, Quantity(0, 'mL'))
            assert "must be greater than 0" in str(e.value)
            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, Quantity(-1, 'g'))
            assert "must be greater than 0" in str(e.value)
            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, Quantity(-1, 'mL'))
            assert "must be greater than 0" in str(e.value)

            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, 0)
            assert "must be 1 or greater" in str(e.value)
            with pytest.raises(ValueError) as e:
                recipe.add_ingredient(kit.Food.Bread.BASE, -1)
            assert "must be 1 or greater" in str(e.value)
                
        class TestAddMass:

            def test_good_mass(self):
                recipe = kit.Recipe("name")
                mass = Quantity(5, 'g')
                recipe.add_ingredient(kit.Food.Dairy.EGG, mass)

                ingredient = recipe.ingredients[0]

                assert len(recipe.ingredients) == 1
                assert len(ingredient) == 2
                assert ingredient[0] == kit.Food.Dairy.EGG
                assert ingredient[1] == mass

        class TestAddVolume:
            
            def test_vol_in_LUT(self):
                recipe = kit.Recipe("name")

                vol = Quantity(5, 'mL')
                recipe.add_ingredient(kit.Food.Dairy.MILK, vol)

                ingredient = recipe.ingredients[0]
                # print(recipe.ingredients)

                assert len(recipe.ingredients) == 1
                assert ingredient[0] == kit.Food.Dairy.MILK
                assert ingredient[1] == vol
                assert ingredient[2] == Quantity(1.03, "g/mL")


            
            def test_vol_not_in_LUT_no_density(self):

                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                recipe.add_ingredient(kit.Food.Meat.STEAK, vol)

                ingredient = recipe.ingredients[0]

                assert len(recipe.ingredients) == 1
                assert len(ingredient) == 2
                assert ingredient[0] == kit.Food.Meat.STEAK
                assert ingredient[1] == vol
                

            def test_vol_not_in_LUT_with_density(self):
                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                density = Quantity(5, 'g/mL')

                recipe.add_ingredient(kit.Food.Meat.CHICKEN, vol, density)

                ingredient = recipe.ingredients[0]

                assert len(recipe.ingredients) == 1
                assert len(ingredient) == 3
                assert ingredient[0] == kit.Food.Meat.CHICKEN
                assert ingredient[1] == vol
                assert ingredient[2] == density
                
            def test_vol_density_not_in_LUT_bad_density(self):
                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                density = Quantity(5, 'g')

                with pytest.raises(ValueError) as e:
                    recipe.add_ingredient(kit.Food.Meat.BASE, vol, density)
                assert "'amount' must be in units of density" in str(e.value)

        class TestAddInt:

            def test_int(self):
                recipe = kit.Recipe("name")
                recipe.add_ingredient(kit.Food.Meat.BASE, 1)

                ingredient = recipe.ingredients[0]

                assert len(recipe.ingredients) == 1
                assert len(ingredient) == 2
                assert ingredient[0] == kit.Food.Meat.BASE
                assert ingredient[1] == 1

    class TestRecipes:
        " Not sure which cases to do here"
        def test_short_good(self):

            ingredients = [
                [kit.Food.Dairy.MILK, Quantity(1, "cup"), Quantity(1.03, "g/mL")],
                [kit.Food.Spice.SALT, Quantity(1, "tbsp")],
                [kit.Food.Meat.CHICKEN, Quantity(0.5, "pound")],
                [kit.Food.Fruit.STRAWBERRY, Quantity(5, "oz")]
            ]

            recipe = kit.Recipe.from_ingredients("name", ingredients)

            assert len(recipe.ingredients) == 4
            for expected, actual in zip(ingredients, recipe.ingredients):
                assert expected == actual

        def test_short_err(self):

            ingredients = [
                [kit.Food.Dairy.MILK, Quantity(1, "cup"), Quantity(1.03, "g/mL")],
                [kit.Food.Spice.SALT, Quantity(1, "tbsp")],
                [kit.Food.Meat.CHICKEN, Quantity(0.5, "pound")],
                [kit.Food.Fruit.STRAWBERRY, Quantity(5, "meter")]
            ]

            with pytest.raises(ValueError):
                kit.Recipe.from_ingredients("name", ingredients)

    class TestGetIngredients:

        @staticmethod
        def recipe_factory(name = None, ingredients = None):
            """ Returns (recipe, ingreeitns)"""
            if ingredients is None:
                ingredients = [
                    [kit.Food.Dairy.MILK, Quantity(1, "cup"), Quantity(1.03, "g/mL")],
                    [kit.Food.Spice.SALT, Quantity(1, "tbsp")],
                    [kit.Food.Meat.CHICKEN, Quantity(0.5, "pound")],
                    [kit.Food.Fruit.STRAWBERRY, Quantity(5, "oz")]
                ]

            if name is None:
                name == "name"
            
            return kit.Recipe.from_ingredients(name, ingredients), ingredients

        def test_serving_size_1(self):
            recipe, ingredients = self.recipe_factory()

            result = recipe.get_ingredients()

            assert len(recipe.ingredients) == 4
            for expected, actual in zip(ingredients, result):
                assert expected == actual

        def test_serving_size_100(self):

            ingredients_times_100 = [
                    [kit.Food.Dairy.MILK, Quantity(100, "cup"), Quantity(1.03, "g/mL")],
                    [kit.Food.Spice.SALT, Quantity(100, "tbsp")],
                    [kit.Food.Meat.CHICKEN, Quantity(50, "pound")],
                    [kit.Food.Fruit.STRAWBERRY, Quantity(500, "oz")]
                ]
            

            recipe, ingredients = self.recipe_factory()

            result = recipe.get_ingredients(100)

            assert len(recipe.ingredients) == 4
            for expected, actual in zip(ingredients_times_100, result):
                assert expected == actual

        def test_serving_size_0_01(self):

            ingredients_times_100 = [
                    [kit.Food.Dairy.MILK, Quantity(1 / 1000, "cup"), Quantity(1.03, "g/mL")],
                    [kit.Food.Spice.SALT, Quantity(1 / 1000, "tbsp")],
                    [kit.Food.Meat.CHICKEN, Quantity(0.5 / 1000, "pound")],
                    [kit.Food.Fruit.STRAWBERRY, Quantity(5 / 1000, "oz")]
                ]
            

            recipe, _ = self.recipe_factory()

            result = recipe.get_ingredients(0.001)

            assert len(recipe.ingredients) == 4
            for expected, actual in zip(ingredients_times_100, result):
                assert expected == actual

        def test_serving_size_7(self):

            ingredients_times_7 = [
                    [kit.Food.Dairy.MILK, Quantity(1 * 7, "cup"), Quantity(1.03, "g/mL")],
                    [kit.Food.Spice.SALT, Quantity(1 * 7, "tbsp")],
                    [kit.Food.Meat.CHICKEN, Quantity(0.5 * 7, "pound")],
                    [kit.Food.Fruit.STRAWBERRY, Quantity(5 * 7, "oz")]
                ]
            

            recipe, _ = self.recipe_factory()

            result = recipe.get_ingredients(7)

            assert len(recipe.ingredients) == 4
            for expected, actual in zip(ingredients_times_7, result):
                assert expected == actual
    
    class TestTools:
        def test_non_string(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError):
                recipe.add_tool(1)
                
            assert len(recipe.tools) == 0

        def test_not_in_tools(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError):
                recipe.add_tool(kit.Food.Drink)
                
            assert len(recipe.tools) == 0

        def test_tools(self):
            tools = [
                kit.Tool.Knife.BUTTER,
                kit.Tool.BLENDER,
                kit.Tool.Mixer.STAND
            ]
            recipe = kit.Recipe("name")

            for tool in tools:
                recipe.add_tool(tool)
                
            assert len(recipe.tools) == 3
            for expected, actual in zip(tools, recipe.tools):
                assert expected == actual


    class TestSteps:

        def test_add_steps(self):
            steps = [
                "step 1",
                "step 2",
                "step 3",
                "step 4",
                "step 5",
                "step 6"
            ]
            recipe = kit.Recipe("name")

            for step in steps:
                recipe.add_step(step)

            assert recipe.steps == steps

        def test_add_steps_non_string(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError):
                recipe.add_step(1)
                
            assert len(recipe.steps) == 0


            








