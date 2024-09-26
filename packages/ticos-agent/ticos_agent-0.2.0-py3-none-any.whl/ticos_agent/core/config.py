import yaml
import os


class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_dir = os.path.dirname(os.path.abspath(config_path))
        self._config = {}
        self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as file:
            self._config = yaml.safe_load(file)

        self.devices = self._config.get("devices", [])
        self.collection_interval = self._config.get("collection_interval", 60)
        self.custom_robots_path = self._config.get(
            "custom_robots_path", "examples/custom_robots"
        )
        self.otlp_endpoint = self._config.get("otlp_endpoint", "localhost:4317")

        if not os.path.isabs(self.custom_robots_path):
            self.custom_robots_path = os.path.join(
                self.config_dir, self.custom_robots_path
            )

        self.custom_robots_path = os.path.normpath(self.custom_robots_path)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def __getitem__(self, key):
        return self._config[key]

    def __contains__(self, key):
        return key in self._config

    def __str__(self):
        return str(self._config)

    def __repr__(self):
        return f"Config({self.config_path})"
