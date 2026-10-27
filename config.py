import json
import os

CONFIG_FILE = "config.json"


def load_config():
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    source_folder = config.get("source_folder")
    interval = config.get("backup_interval_minutes")

    if not source_folder or not os.path.isdir(source_folder):
        raise ValueError("Source folder does not exist.")

    if not isinstance(interval, int) or isinstance(interval, bool) or interval <= 0:
        raise ValueError("Backup interval must be a positive integer.")

    return config