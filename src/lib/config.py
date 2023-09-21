from os import environ

import yaml

DEFAULT_CONFIG_PATH = "../assets/config.yaml"


# class that reads the config from yaml file
# @usage: value = Config().get("key")
class Config:
    __instance = None

    def __init__(self):
        self.config_path = environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)
        self.values: dict = self.load_config()

    @staticmethod
    def instance():
        """
        Singleton method
        :return: config class
        """
        if not Config.__instance:
            Config.__instance = Config()
        return Config.__instance

    def load_config(self):
        """
        loads the config from yaml
        :return: config dictionary
        """
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def all(self) -> dict:
        """
        gets the config values
        :return: config dictionary
        """
        return self.values

    def get(self, key):
        """
        gets a key from the config
        :param key: dict key
        :return: dict value
        """
        return self.values.get(key, {})
