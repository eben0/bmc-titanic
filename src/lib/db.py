import sqlite3

# from flask import g, current_app
import pandas as pd
import logging

from lib.config import Config

logger = logging.getLogger(__name__)

# db class to wrap the sqlite object
class Db:
    __instance = None
    __client = None
    DEFAULT_LIMIT = 100

    def __init__(self):
        self.config = Config.instance().get("db")

    @staticmethod
    def instance():
        if not Db.__instance:
            Db.__instance = Db()
        return Db.__instance

    def get_db(self):
        db = Db.__client
        if db is None:
            logger.info("initiating database")
            Db.__client = db = sqlite3.connect(
                self.config.get("file"), check_same_thread=False
            )
            db.row_factory = Db.dict_factory
        return db

    def cursor(self):
        return self.get_db().cursor()

    def init_db(self):
        self.import_csv()

    def import_csv(self):
        logger.info("importing into Sqlite from CSV")
        conn = self.get_db()
        df = pd.read_csv(self.config.get("csv"))
        df.to_sql(self.config.get("table"), conn, if_exists="append", index=False)

    @staticmethod
    def dict_factory(cursor, row):
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    @staticmethod
    def get_limit(limit=DEFAULT_LIMIT):
        try:
            if limit is None:
                return Db.DEFAULT_LIMIT
            return int(limit)
        except ValueError:
            return Db.DEFAULT_LIMIT
