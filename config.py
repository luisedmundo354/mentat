import os
import yaml

def load_config():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config', 'settings.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

CONFIG = load_config()