import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../..")) # To get KitchenInventory
# sys.path.insert(1, os.getcwd()) # Assumes running in root

import KitchenInventory as kit
import pytest
from pint import Quantity
# import pandas as pd
# from datetime import datetime, timedelta
# import numpy as np


########################################################################
#                              Inventory                               #
########################################################################

class TestInventory:

    def test_constructor(self):
        inv = kit.Inventory("name")
        assert inv.name == "name"
        assert len(inv.food_objs) == 0
        necessary_columns = ["Name", "Food Type", "Mass (g)", "Volume (mL)", "Density (g/mL)", "Amount", "Expiration"]
        for col in necessary_columns:
            assert col in list(inv.foods.columns)

    class TestAddItem:
        """
        Adds Name, Food Type, Amount, Expiration by default
        Should add Mass, Volume, Density for Item
        Should add Amount for CountableItenm
        """

        def test_Item_no_expiration(self):
            """Should add mass, volume, density be default"""
            name = "item"
            food_type = "bread"
            mass=Quantity(5, "g")
            item = kit.Item(name,
                            food_type=food_type,
                            mass=mass)
            inv = kit.Inventory("name")
            inv.add_item(item)
            
            row = inv.foods.iloc[0,:]

            # Common columns
            assert row["Name"] == name
            assert row["Food Type"] == food_type
            assert row["Amount"] == 1
            assert row["Expiration"] == ""

            # Item columns
            assert float(row["Mass (g)"]) == mass.m
            assert float(row["Density (g/mL)"]) == 1.0
            assert float(row["Volume (mL)"]) == mass.m # Turning unitless

        def test_Item_with_expiration(self):
            """Should add mass, volume, density be default"""
            name = "item"
            food_type = "bread"
            mass = Quantity(5, "g")
            expiration = "2024-03-04"
            item = kit.Item(name,
                            food_type=food_type,
                            mass=mass,
                            expiration=expiration)
            inv = kit.Inventory("name")
            inv.add_item(item)
            
            row = inv.foods.iloc[0,:]

            assert row["Expiration"] == expiration

        def test_CountableItem_no_expiration(self):
            """Should add mass, volume, density be default"""
            name = "item"
            food_type = "bread"
            quantity = 7
            item = kit.CountableItem(name,
                            food_type=food_type,
                            quantity=quantity)
            inv = kit.Inventory("name")
            inv.add_item(item)
            
            row = inv.foods.iloc[0,:]

            # Common columns
            assert row["Name"] == name
            assert row["Food Type"] == food_type
            assert row["Amount"] == "7"
            assert row["Expiration"] == ""

    class TestAddItems:

        def test_multiple_items_no_details(self):
            """ Big example """
            items: list[kit.Item | kit.CountableItem] = [
                kit.Item(
                    "Heavy milk",
                    kit.Food.Dairy.MILK,
                    mass=Quantity(5, "lb"),
                    density=Quantity(5, "g / mL"),
                    expiration="2025-05-30"
                    ),
                kit.Item(
                    "Milk", 
                    kit.Food.Dairy.MILK,
                    volume=Quantity(5, "liter"),
                    expiration="1025-05-30"),
                kit.CountableItem(
                    "egg.", 
                    kit.Food.Dairy.EGG,
                    12)
            ]

            inv = kit.Inventory("name")
            inv.add_items(items)

            name_col = inv.foods["Name"]
            type_col = inv.foods["Food Type"]
            mass_col = inv.foods["Mass (g)"]
            vol_col = inv.foods["Volume (mL)"]
            density_col = inv.foods["Density (g/mL)"]
            amount_col = inv.foods["Amount"]
            expiration_col = inv.foods["Expiration"]

            assert list(name_col) == ["Heavy milk", "Milk", "egg."]
            assert list(type_col) == [
                kit.Food.Dairy.MILK,
                kit.Food.Dairy.MILK,
                kit.Food.Dairy.EGG
            ]

            def compare_cols(expected: list, actual: list):
                actual = [float(i) if i != "" else None for i in actual]
                for i,j in zip(actual, expected):
                    assert i == pytest.approx(j)

            expected_mass = [2267.96185, 5000, None] # g
            compare_cols(expected_mass, list(mass_col))

            expected_volume = [453.59237, 5000, None] # mL
            compare_cols(expected_volume, list(vol_col))

            expected_density = [5, 1, None] # g/mL
            compare_cols(expected_density, list(density_col))

            expected_amount = [1, 1, 12] # g/mL
            compare_cols(expected_amount, list(amount_col))

            expected_expiration = ["2025-05-30", "1025-05-30", ""] # g/mL
            assert list(expiration_col) == expected_expiration

            for col in kit.Inventory.columns + kit.Inventory.details_columns:
                assert col in list(inv.foods.columns)

    # class TestRowToItem:

    #     def test_simple(self):
    #         item = kit.Item("name", "bread", mass=Quantity(5, "kg"))

    #         row = pd.DataFrame.from_dict({
    #             "Name": "name",
    #             "Food Type": "/dairy",
    #         })


# TODO