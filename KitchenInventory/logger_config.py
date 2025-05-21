import logging
import yaml
import logging.config

def load_yaml(filename: str) -> dict:
    with open(filename) as f:
        file = yaml.safe_load(f)
    return file
    
def setup_logging(config_yaml: dict):
    logging.config.dictConfig(config_yaml["logging"])
    logging.getLogger(__name__).info("Loaded logger")
