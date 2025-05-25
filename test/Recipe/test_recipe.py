import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../..")) # To get KitchenInventory

import KitchenInventory as kit
import pytest
from pint import Quantity


########################################################################
#                                  Recipe                              #
########################################################################

class TestRecipe:

    def test_constructor(self):

        recipe = kit.Recipe("name")

        assert recipe.name == "name"
        assert recipe.ingredients == []

    class TestAddIngredient:

        def test_bad_food_type(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError) as e:
                recipe.add_ingredient("name", 0)
            assert "food_type not in foods" in str(e.value)

        def test_bad_type(self):
            recipe = kit.Recipe("name")

            with pytest.raises(ValueError) as e:
                recipe.add_ingredient("/bread", 0.0)
            assert "type not 'int' or 'Quantity'" in str(e.value)

        def test_0_or_less(self):
            recipe = kit.Recipe("name")
            with pytest.raises(ValueError):
                recipe.add_ingredient("/bread", Quantity(0, 'g'))
            with pytest.raises(ValueError):
                recipe.add_ingredient("/bread", Quantity(0, 'mL'))
                
        class TestAddMass:

            def test_good_mass(self):
                pass

        class TestAddVolume:
            
            def test_vol_in_LUT(self):
                recipe = kit.Recipe("name")

                vol = Quantity(5, 'mL')
                recipe.add_ingredient("/dairy/milk", vol)

                ingredient = recipe.ingredients[0]
                # print(recipe.ingredients)

                assert ingredient[0] == "/dairy/milk"
                assert ingredient[1] == vol
                assert ingredient[2] == Quantity(1.03, "g/mL")


            
            def test_vol_not_in_LUT_no_density(self):

                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                recipe.add_ingredient("/dairy/egg", vol)

                ingredient = recipe.ingredients[0]

                assert ingredient[0] == "/dairy/egg"
                assert ingredient[1] == vol
                assert ingredient[2] is None
                

            def test_vol_not_in_LUT_with_density(self):
                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                density = Quantity(5, 'g/mL')

                recipe.add_ingredient("/dairy/egg", vol, density)

                ingredient = recipe.ingredients[0]

                assert ingredient[0] == "/dairy/egg"
                assert ingredient[1] == vol
                assert ingredient[2] == density
                
            def test_vol_density_not_in_LUT_bad_density(self):
                recipe = kit.Recipe("name")
                vol = Quantity(5, 'mL')
                density = Quantity(5, 'g')

                with pytest.raises(ValueError) as e:
                    recipe.add_ingredient("/meat", vol, density)
                assert "'amount' must be in units of density" in str(e.value)
            


