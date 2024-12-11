import json
import os

APP_DIR = "aliasaurus"


class ConfigFile:
    """A generic configuration file that can be saved and loaded from disk."""

    def __init__(self, name: str):
        self.name = name
        self.path = os.path.join(os.environ["APPDATA"], APP_DIR, name)

    def load(self) -> dict:
        """Loads the configuration file from disk into a dictionary."""
        if not os.path.exists(self.path):
            return {}
        with open(self.path) as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def save(self, data: dict):
        """Saves the configuration file to disk."""
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as file:
            file.write(json.dumps(data, indent=4))
