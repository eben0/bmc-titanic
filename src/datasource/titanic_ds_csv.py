import logging
from typing import List, Dict

import pandas as pd
from pandas import DataFrame

from lib.config import Config

logger = logging.getLogger()


# CSV datasource
class TitanicDatasourceCSV:
    def __init__(self):
        self.config = Config.instance().all()
        self.csv_df = self.read_csv_df()

    def get_passengers(self, id=None, cols="", limit=1) -> List[Dict]:
        """
        gets passengers from csv as dataframe
        :param id: passenger id
        :param cols: list column separated by comma
        :param limit: number of records to return
        :return: passengers list
        """
        if id:
            # get by id
            results = self.csv_df.loc[self.csv_df["PassengerId"] == int(id)]
        else:
            results = self.csv_df.iloc[0 : int(limit)]
        if cols != "*":
            cols = cols.split(",")
            # filter the cols
            results = results[[*cols]]
        return results.fillna(0).to_dict("records")

    def get_prices(self):
        return self.csv_df[["Fare"]]

    def read_csv_df(self) -> DataFrame:
        """
        reads csv into dataframe
        :return: pandas dataframe
        """
        try:
            return pd.read_csv(self.config.get("db", {}).get("csv"))
        except Exception as e:
            logger.error("Unable to load records from csv")
        return pd.DataFrame.from_records([])
