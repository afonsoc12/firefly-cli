import configparser
import os
from pathlib import Path

from xdg.BaseDirectory import xdg_config_home

if os.getenv("FIREFLY_CLI_CONFIG"):
    config_file_path = Path(os.environ["FIREFLY_CLI_CONFIG"])
else:
    config_file_path = Path(xdg_config_home).joinpath("firefly-cli", "firefly-cli.ini")

    # Create dir if not exists
    config_file_path.parent.mkdir(parents=True, exist_ok=True)


def load_configs():
    configs = configparser.ConfigParser()

    # No config file loaded because it was not available/not existent
    if len(configs.read(config_file_path)) < 1:
        print("File not found, creating the file..")

        with open(config_file_path, "w") as f:
            configs["API"] = {}
            save_configs_to_file(configs)

    return configs


def save_configs_to_file(configs):
    try:
        with open(config_file_path, "w") as f:
            configs.write(f)
            print("Config file saved at {}".format(str(config_file_path)))
    except:
        print(
            "An error has occurred while saving file to {}".format(
                str(config_file_path)
            )
        )
