import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], "../../..")) # To get KitchenInventory

# from fastapi import FastAPI
from fastapi.testclient import TestClient
from urllib.parse import urlencode, quote, unquote

import KitchenInventory as kit
from KitchenInventory.server import app

CURR_DIR = os.getcwd()

try:
    os.remove(f"{CURR_DIR}/inventories/custom_name.csv")
except OSError:
    pass

try:
    os.remove(f"{CURR_DIR}/inventories/000_new_name_saved.csv")
except OSError:
    pass

try:
    os.remove(f"{CURR_DIR}/inventories/BAD_FILE")
except OSError:
    pass

client = TestClient(app)

def test_root():
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == {"msg": "Inventory! Do things here"}

########################################################################
#                       With no inventory loaded                       #
########################################################################

def test_list_no_inventory():

    response = client.get("/inventory/list-items")
    assert response.status_code == 400
    assert response.json() == {"detail": "Inventory not loaded"}

def test_add_no_inventory():

    # Adding steak
    data = {
        "name": "Skirt Steak",
        "food_type": "meat-beef-steak",
        "mass": "8 oz",
        "density": "1.06 g/ml"
    }
    response = client.post("/inventory/add-item", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Inventory not loaded"}
    
########################################################################
#                            Create and Save                           #
########################################################################

class TestCreateAndSave:

    def test_create_new_name(self):
        params = {
            "name": "new_name"
        }
        response = client.put(f"/inventory/create?{urlencode(params)}")
        assert response.status_code == 200
        assert response.json() == {"msg": f"Created Inventory '{params["name"]}'"}

    # Creates '000_new_name_saved.csv'
    def test_new_name(self):
        params = {
            "name": "000_new_name_saved"
        }
        inventory = kit.Inventory(params["name"])
        client.put(f"/inventory/create?{urlencode(params)}")

        response = client.put("inventory/save")
        assert response.status_code == 200
        assert response.json() == {"status": "Saved",
                                   "filename": f"{CURR_DIR}/inventories/{inventory.name}.csv"}

    # Creates 'custom_name.csv'   
    def test_custom_name(self):
        inventory = kit.Inventory("name")
        params = {"name": inventory.name}
        client.put(f"/inventory/create?{urlencode(params)}")

        params = {"name": "custom_name"} 
        response = client.put(f"inventory/save?{urlencode(params)}")
        assert response.status_code == 200
        assert response.json() == {"status": "Saved",
                                   "filename": f"{CURR_DIR}/inventories/{params["name"]}.csv"}

    def test_inventory_exists(self):
        inventory = kit.Inventory("000_new_name_saved")
        params = {"name": inventory.name} 

        response = client.put(f"/inventory/create?{urlencode(params)}")
        assert response.status_code == 200
        assert response.json() == {"msg": f"Found '000_new_name_saved.csv' and loaded into Inventory '{inventory.name}'"}

class TestList:

    def test_two_inventories(self):
        response = client.get("/inventory/list")
        assert response.status_code == 200

        inventory_list = response.json()["inventories"]

        assert len(inventory_list) >= 2
        for i,val in enumerate(inventory_list):
            assert val[0] == i
            
        assert "000_new_name_saved.csv" in [i[1] for i in inventory_list]
        assert "custom_name.csv" in [i[1] for i in inventory_list]

class TestSelect:

    def test_out_of_bounds(self):
        params = {"num": -1} 
        response = client.put(f"/inventory/select?{urlencode(params)}")
        assert response.status_code == 400
        assert "'-1' out of range of inventory numbers" in response.json()["detail"]

        params = {"num": 10000} 
        response = client.put(f"/inventory/select?{urlencode(params)}")
        assert response.status_code == 400
        assert "'10000' out of range of inventory numbers" in response.json()["detail"]

    def test_select_000_new_name_saved(self):
        response = client.get("/inventory/list")
        assert response.status_code == 200

        inventory_list = response.json()["inventories"]

        inventory_num = [i[0] for i in inventory_list if i[1] == "000_new_name_saved.csv"][0]
        
        params = {"num": inventory_num} 
        response = client.put(f"/inventory/select?{urlencode(params)}")
        assert response.status_code == 200
        assert response.json() == {"msg": "Loaded '000_new_name_saved.csv' into Inventory '000_new_name_saved'"}

    def test_create_badly_formatted_inventory(self):
        filepath = f"{CURR_DIR}/inventories/BAD_FILE"
        with open(filepath, "w") as file:
            file.write("test\ntest")

        response = client.get("/inventory/list")
        assert response.status_code == 200

        inventory_list = response.json()["inventories"]
        inventory_num = [i[0] for i in inventory_list if i[1] == "BAD_FILE"][0]
        
        params = {"num": inventory_num} 
        response = client.put(f"/inventory/select?{urlencode(params)}")
        assert response.status_code == 400

class TestListAndAddItems:

    def load_inv(self, name: str):
        response = client.get("/inventory/list")
        assert response.status_code == 200
        inventory_list = response.json()["inventories"]
        inventory_num = [i[0] for i in inventory_list if i[1] == f"{name}.csv"][0]

        params = {"num": inventory_num} 
        response = client.put(f"/inventory/select?{urlencode(params)}")
        assert response.status_code == 200
        assert response.json() == {"msg": f"Loaded '{name}.csv' into Inventory '{name}'"}

    def test_add_good_with_objects(self):
        self.load_inv("000_new_name_saved")

        # Adding steak
        data = {
            "name": "Skirt Steak",
            "food_type": "meat-beef-steak",
            "mass": "8 oz",
            "density": "1.06 g/ml"
        }
        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 200
        assert response.json()["status"] == "Added item"

        # Adding steak
        data = {
            "name": "Chicken",
            "food_type": "meat-chicken",
            "mass": "12 oz",
            "density": "1.06 g/ml"
        }
        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 200
        assert response.json()["status"] == "Added item"


        # List should be 2 long
        params = {"objects": True} 
        response = client.get(f"/inventory/list-items?{urlencode(params)}")
        assert response.status_code == 200
        assert list(response.json().keys()) == ["items"]
        items = response.json()["items"]

        assert len(items) == 2
        assert "['Skirt Steak' - meat-beef-steak: " in items[0]
        assert "['Chicken' - meat-chicken: " in items[1]

    def test_list_with_dict(self):

        # List should be 2 long
        params = {"objects": False} 
        response = client.get(f"/inventory/list-items?{urlencode(params)}")
        assert response.status_code == 200
        assert list(response.json().keys()) == ["items"]
        items = response.json()["items"]

        assert items["Name"] == {"0": "Skirt Steak", "1": "Chicken"}
        assert items["Food Type"] == {"0": "meat-beef-steak", "1": "meat-chicken"}
        assert items["Density (g/mL)"] == {"0": "1.06", "1": "1.06"}

    def test_add_bad_mass(self):
        self.load_inv("000_new_name_saved")

        data = {
            "name": "Chicken",
            "food_type": "meat-chicken",
            "mass": "12oz",
        }

        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": f"Mass '{data["mass"]}' must contain the format '# unit'"}

    def test_add_bad_volume(self):
        self.load_inv("000_new_name_saved")

        data = {
            "name": "Chicken",
            "food_type": "meat-chicken",
            "mass": "12 oz",
            "volume": "12mL"
        }

        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": f"Volume '{data["volume"]}' must contain the format '# unit'"}
    
    def test_add_bad_density(self):
        self.load_inv("000_new_name_saved")

        data = {
            "name": "Chicken",
            "food_type": "meat-chicken",
            "mass": "12 oz",
            "density": "12g/mL"
        }

        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": f"Density '{data["density"]}' must contain the format '# unit'"}

    def test_add_bad_food_type(self):
        self.load_inv("000_new_name_saved")

        data = {
            "name": "Chicken",
            "food_type": "meat/chicken",
            "mass": "12 oz",
        }

        response = client.post("/inventory/add-item", json=data)
        assert response.status_code == 400
        assert response.json() == {"detail": f"Food type '{data["food_type"]}' must be in foods list"}





