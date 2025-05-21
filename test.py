from KitchenInventory.logger_config import setup_logging, load_yaml
import logging

# Setting up logging
yamlfile = load_yaml("./config.yaml")
config = setup_logging(yamlfile)
logger = logging.getLogger(__name__)

import KitchenInventory as kit  # noqa: E402
from pint import Quantity  # noqa: E402

a = kit.Item("thing", volume=Quantity(5, "mL"), density=Quantity(5, "g / mL"))
b = kit.Item("thing", volume=Quantity(5, "mL"))
c = kit.CountableItem("egg", 5)