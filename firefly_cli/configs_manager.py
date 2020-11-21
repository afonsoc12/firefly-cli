import json
from pathlib import Path

config_file_path = Path(__file__).parents[1].joinpath('firefly-cli.json')

def load_configs():
    try:
        with open(config_file_path, 'r') as f:
            configs = json.loads(f.read())
    except FileNotFoundError:
        print('File not found, creating the file..')

        with open(config_file_path, 'w') as f:
            configs = {'URL': None, 'API_TOKEN': None}
            save_configs_to_file(configs)
    return configs


def save_configs_to_file(configs):
    try:
        with open(config_file_path, 'w') as f:
            json.dump(configs, f)
            print('Config file saved at {}'.format(str(config_file_path)))
    except:
        print('An error has occurred while saving file to {}'.format(str(config_file_path)))

