#!/usr/bin/env python
#  coding=utf-8

import json
from pathlib import Path
from running_modes.manager import Manager

DEFAULT_BASE_CONFIG_PATH = (Path(__file__).parent / 'configs/config.json').resolve()

def read_json_file(path):
    with open(path) as f:
        json_input = f.read().replace('\r', '').replace('\n', '')
    try:
        return json.loads(json_input)
    except (ValueError, KeyError, TypeError) as e:
        print(f"JSON format error in file ${path}: \n ${e}")


# New wrapper function
def run_reinvent(run_config_path, base_config_path=None):
    """
    Function to run REINVENT with the given configuration.
    
    :param run_config_path: Path to the run configuration JSON file
    :param base_config_path: Path to the base configuration file (optional)
    """
    if base_config_path is None:
        base_config_path = DEFAULT_BASE_CONFIG_PATH

    base_config = read_json_file(base_config_path)
    run_config = read_json_file(run_config_path)

    manager = Manager(base_config, run_config)
    manager.run()
