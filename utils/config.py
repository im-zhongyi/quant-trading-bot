# utils/config_loader.py
import yaml

def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def get_config_filepath(yaml_name: str) -> dict:
    return f"config/{yaml_name}.yaml"
    # return load_yaml(path)