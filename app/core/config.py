from pathlib import Path
import yaml
class Config:
    def __init__(self, file_path="config.yaml"):
        self.file_path = Path(file_path)
        self.data = self.load_config()

    def load_config(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.file_path}")

        with open(self.file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get(self, section, key):
        return self.data[section][key]




