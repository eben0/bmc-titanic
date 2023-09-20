import os
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
            db_file = os.path.realpath(self.config.get("file"))
            logger.info(f"Connecting to db {db_file}")
            folder = os.path.dirname(db_file)
            if not os.path.exists(folder):
                os.mkdir(folder)
            try:
                Db.__client = db = sqlite3.connect(db_file, check_same_thread=False)
                db.row_factory = Db.dict_factory
            except sqlite3.OperationalError as e:
                logger.error(e)
                raise e
        return db

    def cursor(self):
        return self.get_db().cursor()

    def init_db(self):
        self.import_csv()

    def import_csv(self):
        try:
            csv_file = self.config.get("csv")
            logger.info(f"importing into Sqlite from CSV {csv_file}")
            conn = self.get_db()
            df = pd.read_csv(csv_file)
            df.to_sql(self.config.get("table"), conn, if_exists="append", index=False)
            logger.info(f"import finished")
        except ValueError as e:
            logger.error("Unable to import CSV", e)

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
