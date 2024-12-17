import json
import os

DEFAULT_THEME = "light"
SETTINGS_PATH = os.path.join(os.environ["APPDATA"], "aliasaurus", "settings.json")


class Settings:
    """Settings for the application. These are saved to disk and loaded on startup."""

    def __init__(self, theme: str = DEFAULT_THEME):
        self.theme = theme

    def set_theme(self, value: str):
        self.theme = value
        self.save()

    def load(self) -> None:
        if not os.path.exists(SETTINGS_PATH):
            self._from_json({})
            return
        with open(SETTINGS_PATH) as file:
            try:
                self._from_json(json.load(file))
            except json.JSONDecodeError:
                self._from_json({})

    def save(self):
        if not os.path.exists(os.path.dirname(SETTINGS_PATH)):
            os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w") as file:
            json.dump(self._to_json(), file)

    def _to_json(self):
        return {"theme": self.theme}

    def _from_json(self, json: dict):
        if "theme" in json:
            self.theme = json["theme"]
