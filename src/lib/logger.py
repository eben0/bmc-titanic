import logging

from .config import Config

config = Config.instance().get("logger")


# setup logger
class Logger:
    @staticmethod
    def setup():
        logging.basicConfig(
            format="%(asctime)s [%(levelname)-4s] %(message)s",
            level=config.get("level", logging.INFO),
            datefmt="%d-%m-%Y %H:%M:%S",
        )
