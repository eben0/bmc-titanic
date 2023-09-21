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

    def __init__(self):
        self.config = Config.instance().get("db")

    @staticmethod
    def instance():
        """
        Singleton
        :return: Db class
        """
        if not Db.__instance:
            Db.__instance = Db()
        return Db.__instance

    def get_db(self):
        """
        gets sqlite db instance if created,
        otherwise open/create the file and open a connection
        :return:
        """
        db = Db.__client
        if db is None:
            # gets the file path from config
            db_file = os.path.realpath(self.config.get("file"))
            logger.info(f"Connecting to db {db_file}")
            # create dir if not exists
            folder = os.path.dirname(db_file)
            if not os.path.exists(folder):
                os.mkdir(folder)
            try:
                # connect and set the client
                Db.__client = db = sqlite3.connect(db_file, check_same_thread=False)
                db.row_factory = Db.dict_factory
            except sqlite3.OperationalError as e:
                logger.error(e)
                # raise the error in order to crash the app
                raise e
        return db

    def cursor(self):
        """
        cursor shortcut
        :return: Cursor
        """
        return self.get_db().cursor()

    def init_db(self):
        """
        init the db by importing data from CSV
        """
        self.import_csv()

    def import_csv(self):
        """
        imports data from CSV using pandas
        """
        try:
            csv_file = self.config.get("csv")
            logger.info(f"importing into Sqlite from CSV {csv_file}")
            conn = self.get_db()
            df = pd.read_csv(csv_file)
            # import the csv, add new entries if they do not exists,
            # otherwise crete the table and insert
            df.to_sql(self.config.get("table"), conn, if_exists="append", index=False)
            logger.info(f"import finished")
        except ValueError as e:
            logger.error("Unable to import CSV", e)

    @staticmethod
    def dict_factory(cursor, row):
        """
        transform the data into a dictionary
        :param cursor: Cursor
        :param row: Row
        :return: dictionary
        """
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}
