import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../..")) # To get KitchenInventory
# sys.path.insert(1, os.getcwd()) # Assumes running in root

import KitchenInventory as kit
import pytest
from pint import Quantity
from datetime import datetime, timedelta
import numpy as np


########################################################################
#                                   Item                               #
########################################################################

class TestItem:
    
    class TestConsturctor:

        class TestBadAttributes:

            def test_bad_expiration(self):
                """ Raised automatically with datetime """
                with pytest.raises(ValueError):
                    expiration = "FAKE"
                    kit.Item("name", "type", expiration=expiration)

            def test_bad_food_type(self):
                """ Food types must be in food list (and start with '/') """
                with pytest.raises(ValueError) as e:
                    food_type = "FAKE"
                    kit.Item("name", food_type)
                assert str(e.value) == f"Food type '{food_type}' must be in foods list"

            def test_bad_mass_type(self):
                """ Mass must be of type Quantity"""
                with pytest.raises(ValueError) as e:
                    mass = "5.0 kg"
                    kit.Item("name", "bread", mass=mass)
                assert str(e.value) == f"Mass must be of type {Quantity} and not {str}"

            def test_bad_volume_type(self):
                """ Mass must be of type Quantity"""
                with pytest.raises(ValueError) as e:
                    volume = "5.0 mL"
                    kit.Item("name", "bread", volume=volume)
                assert str(e.value) == f"Volume must be of type {Quantity} and not {str}"

            def test_bad_volume_type_with_valid_mass(self):
                """ Mass must be of type Quantity"""
                with pytest.raises(ValueError) as e:
                    mass = Quantity(5, "g")
                    volume = "5.0 mL"
                    kit.Item("name", "bread", mass=mass, volume=volume)
                assert str(e.value) == f"Volume must be of type {Quantity} and not {str}"

            def test_bad_density_type(self):
                with pytest.raises(ValueError) as e:
                    mass = Quantity(5, "kg")
                    density = "5.0 g/mL"
                    kit.Item("name", "bread", mass=mass, density=density)
                assert str(e.value) == f"Density must be of type {Quantity} and not {str}"

        class TestValidProperties:

            def test_name_and_expiration(self):
                mass = Quantity(5, "kg")
                name = "milk"
                expiration = "2024-05-02"
                item = kit.Item(name, "bread", mass=mass, expiration=expiration)
                assert item.name == name
                assert item.expiration == datetime.strptime(expiration, "%Y-%m-%d")

            def test_mass(self):
                mass = Quantity(5, "kg")
                item = kit.Item("name", "bread", mass=mass)
                assert item.mass == mass.to("g")
                assert item.density == Quantity(1, "g/mL")
                assert item.volume == (mass / item.density).to("mL")

            def test_mass_density(self):
                mass = Quantity(5, "kg")
                density = Quantity(4, "kg / m^3")
                item = kit.Item("name", "bread", mass=mass, density=density)
                assert item.mass == mass.to("g")
                assert item.density == density.to("g/mL")
                assert item.volume == (mass / item.density).to("mL")

            def test_volume(self):
                volume = Quantity(5, "mL")
                item = kit.Item("name", "bread", volume=volume)
                assert item.volume == volume.to("mL")
                assert item.density == Quantity(1, "g/mL")
                assert item.mass == (volume * item.density).to("g")

            def test_volume_density(self):
                volume = Quantity(5, "gallon")
                density = Quantity(4, "kg / m^3")
                item = kit.Item("name", "bread", volume=volume, density=density)
                assert item.volume == volume.to("mL")
                assert item.density == density.to("g/mL")
                assert kit.approx_qty(item.mass, volume*density)

            def test_mass_volume_density(self):
                mass = Quantity(5, "kg")
                volume = Quantity(5, "gallon")
                item = kit.Item("name", "bread", mass=mass, volume=volume)
                assert item.mass == mass.to("g")
                assert item.volume == volume.to("mL")
                assert kit.approx_qty(item.density, mass/volume)
        class TestInvalidProperties:

            def test_density_only(self):
                density = Quantity(4, "kg / m^3")
                with pytest.raises(ValueError) as e:
                    kit.Item("name", "bread", density=density)
                assert str(e.value) == "If density is provided, must provide mass or volume"

    class TestExpiration:

        def test_no_expiration(self):
            mass = Quantity(5, "kg")
            item = kit.Item("infinite_item", "bread", mass=mass)

            assert item.days_left == np.inf

        def test_negative(self):
            mass = Quantity(5, "kg")
            expiration = "2003-06-13" # My birthday!
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left < 0

        def test_large_positive(self):
            mass = Quantity(5, "kg")
            expiration = "3003-06-13" # My birthday in 1000 years!
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left > 0

        def test_tomorrow(self):
            mass = Quantity(5, "kg")
            tomorrow_date = datetime.today() + timedelta(days=1)
            expiration = tomorrow_date.strftime("%Y-%m-%d")
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left == 1

    class TestMisc:

        def test_item_setting_density(self):
            mass = Quantity(5, "kg")
            density = Quantity(5, "g/mL")
            item = kit.Item("name", "bread", mass=mass)

            with pytest.raises(PermissionError) as e:
                item.density = density
            assert str(e.value) == "Should not be resetting density after initialization"

########################################################################
#                            CountableItem                             #
########################################################################

class TestCountableItem:

    class TestConstructor:

        class TestBadAttributes:
            def test_bad_expiration(self):
                """ Raised automatically with datetime """
                with pytest.raises(ValueError):
                    expiration = "FAKE"
                    kit.CountableItem("name", "type", quantity=1, expiration=expiration)

            def test_bad_food_type(self):
                """ Food types must be in food list (and start with '/') """
                with pytest.raises(ValueError) as e:
                    food_type = "FAKE"
                    kit.CountableItem("name", food_type, quantity=1)
                assert str(e.value) == f"Food type '{food_type}' must be in foods list"

            def test_bad_quantity_type(self):
                with pytest.raises(ValueError) as e:
                    quantity = True
                    kit.CountableItem("name", "bread", quantity=quantity)
                assert str(e.value) == f"Quantity must be int or float, and 0 or greater. Input was '{quantity}' with type '{type(quantity)}'"

            def test_bad_quantity(self):
                """ Cannot be less than 0 (Quantity of 0 stores the details but showing we are "out")"""
                with pytest.raises(ValueError) as e:
                    quantity = -1
                    kit.CountableItem("name", "bread", quantity=quantity)
                assert str(e.value) == f"Quantity must be int or float, and 0 or greater. Input was '{quantity}' with type '{type(quantity)}'"

        class TestValidProperties:
            
            def test_zero_quantity(self):
                quantity = 0
                item = kit.CountableItem("name", "bread", quantity=quantity)
                assert item.quantity == quantity

            def test_good_quantities(self):
                quantity = 1
                item = kit.CountableItem("name", "bread", quantity=quantity)
                assert item.quantity == quantity

                quantity = 1000000000
                item = kit.CountableItem("name", "bread", quantity=quantity)
                assert item.quantity == quantity

                quantity = 1.5
                item = kit.CountableItem("name", "bread", quantity=quantity)
                assert item.quantity == quantity
        

    class TestExpiration:

        def test_no_expiration(self):
            mass = Quantity(5, "kg")
            item = kit.Item("infinite_item", "bread", mass=mass)

            assert item.days_left == np.inf

        def test_negative(self):
            mass = Quantity(5, "kg")
            expiration = "2003-06-13" # My birthday!
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left < 0

        def test_large_positive(self):
            mass = Quantity(5, "kg")
            expiration = "3003-06-13" # My birthday in 1000 years!
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left > 0

        def test_tomorrow(self):
            mass = Quantity(5, "kg")
            tomorrow_date = datetime.today() + timedelta(days=1)
            expiration = tomorrow_date.strftime("%Y-%m-%d")
            item = kit.Item("infinite_item", "bread", mass=mass, expiration=expiration)

            assert item.days_left == 1