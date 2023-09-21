import logging
from typing import List, Dict

import pandas as pd
from pandas import DataFrame

from lib.config import Config
from lib.db import Db

logger = logging.getLogger()


# sqlite datasource
class TitanicDatasourceDb:
    def __init__(self):
        self.db = Db.instance().get_db()
        self.config = Config.instance().all()

    def get_passengers(self, id=None, cols="", limit=1) -> List[Dict]:
        """
        gets passengers from sqlite
        :param id: passenger id
        :param cols: list column separated by comma
        :param limit: number of records to return
        :return: passengers list
        """
        cur = self.db.cursor()
        if id:
            logger.info(f"Getting passenger with id {id}")
            res = cur.execute(f"SELECT {cols} FROM titanic WHERE PassengerId = ?", [id])
            results = [res.fetchone()]
        else:
            logger.info(f"Getting {limit} passengers")
            res = cur.execute(
                f"SELECT {cols} FROM titanic LIMIT ?",
                [limit],
            )
            results = res.fetchall()
        return results

    def get_prices(self) -> DataFrame:
        """
        gets the data from sqlite
        :return: dataframe of prices
        """
        cur = self.db.cursor()
        res = cur.execute(f"SELECT Fare from titanic")
        return pd.DataFrame.from_records(data=res.fetchall())
