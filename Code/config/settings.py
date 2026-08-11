import json
from pathlib import Path

CONFIG_FILE = Path("config/paths.json")


def load_paths():

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:

        return json.load(file)


PATHS = load_paths()


CARD_DATABASE = Path(PATHS["card_database"])

IMAGE_DATABASE = Path(PATHS["image_database"])
