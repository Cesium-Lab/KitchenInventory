import logging
import yaml
import logging.config
from datetime import datetime

def load_yaml(filename: str) -> dict:
    with open(filename) as f:
        file = yaml.safe_load(f)
    return file

def save_yaml(data: dict, filename: str):
    with open(filename, "w") as f:
        yaml.safe_dump(data, f)
    
def setup_logging(config_yaml: dict):
    # current_time = datetime.now() #TODO: make filelogs better
    # datetime_string = current_time.strftime("%Y%m%d_%H%M")

    logging.config.dictConfig(config_yaml["logging"])
    logging.getLogger(__name__).info("Loaded logger")
