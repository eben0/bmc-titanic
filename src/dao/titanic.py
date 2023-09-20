import logging
from typing import List, Dict

import pandas as pd
from pandas import DataFrame

from dao.schema import titanic_schema
from lib.config import Config
from lib.db import Db

DATA_SOURCE_DB = "db"
DATA_SOURCE_CSV = "csv"

DEFAULT_QUANTILES = [0.25, 0.5, 0.75, 1]

logger = logging.getLogger()


class Titanic:
    def __init__(self):
        self.db = Db.instance().get_db()
        self.config = Config.instance().all()
        self.csv_df = self.read_csv_df()
        self.data_source = self.config.get("dataSource", DATA_SOURCE_DB)

    def get_passengers(self, id, request) -> List[Dict]:
        """
        gets list of passengers
        :param id: passenger id
        :param request: flask request
        :return: list of passengers
        """
        logger.info(f"Calling get_passengers with id {id}")
        # making sure this column exists in the db to avoid injection
        cols = self.filter_qs_cols(request.args.get("cols"))
        limit = Db.get_limit(request.args.get("limit"))
        if self.data_source == DATA_SOURCE_DB:
            return self.get_passengers_from_db(id, cols, limit)
        elif self.data_source == DATA_SOURCE_CSV:
            return self.get_passengers_from_csv(id, cols, limit)

    def get_passengers_from_db(self, id=None, cols="", limit=1) -> List[Dict]:
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
            res = cur.execute(f"SELECT {cols} FROM titanic WHERE PassengerId = ?", [1])
            results = [res.fetchone()]
        else:
            logger.info(f"Getting {limit} passengers")
            res = cur.execute(
                f"SELECT {cols} FROM titanic LIMIT ?",
                [limit],
            )
            results = res.fetchall()
        return results

    def get_passengers_from_csv(self, id=None, cols="", limit=1) -> List[Dict]:
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

    def filter_qs_cols(self, cols: str):
        """
        filters the column names from query string
        :param cols: list column separated by comma
        :return: list of columns
        """
        logger.debug(f"Calling filter_qs_attrs with {cols}")
        query_attrs = "*"
        if cols:
            attrs = cols.split(",")
            for attr in attrs:
                if attr not in titanic_schema:
                    attrs.pop()

            if len(attrs) > 0:
                query_attrs = ",".join(attrs)
        return query_attrs

    def prices_quantile(self, quantiles_str: str):
        """
        gets the quantiles from data source
        :param quantiles_str: list of comma separated quantiles [0.25,0,5]
        :return: histogram list [{x, y}]
        """
        logger.info(f"Calling prices_quantile with {quantiles_str}")
        results = []
        col = "Fare"

        # parsing and validating quantiles from string
        quantiles = self.parse_quantiles_from_string(quantiles_str)
        if not quantiles:
            quantiles = DEFAULT_QUANTILES

        logger.debug(f"using quantiles {quantiles}")

        # gets the prices data as pandas dataframe
        df = self.get_prices_dataframe()
        # calc
        qs = df[col].quantile(quantiles)
        i = 0
        for q in qs:
            results.append({"y": quantiles[i] * 100, "x": q})
            i += 1

        logger.debug(f"prices_quantile result", results)
        return results

    def get_prices_dataframe(self):
        """
        gets the proces as pandas dataframe
        :return: dataframe of prices
        """
        if self.data_source == DATA_SOURCE_DB:
            try:
                # gets the data from sqlite
                return self.get_prices_from_db()
            except Exception as e:
                logger.error("Unable to load records from db", e)
                raise e
        elif self.data_source == DATA_SOURCE_CSV:
            # returns the csv dataframe from memory
            return self.csv_df
        else:
            err = f"{self.data_source} not supported"
            logger.error(err)
            raise err

    def get_prices_from_db(self) -> DataFrame:
        """
        gets the data from sqlite
        :return: dataframe of prices
        """
        cur = self.db.cursor()
        res = cur.execute(f"SELECT Fare from titanic")
        return pd.DataFrame.from_records(data=res.fetchall())

    def parse_quantiles_from_string(self, quantiles_str):
        """
        parsing and validating quantiles from string
        :param quantiles_str:list of comma separated quantiles [0.25,0,5]
        :return: list of quantiles [0.25, 0.5]
        """
        logger.debug(f"parse_quantiles_from_string: {quantiles_str} ")
        quantiles = []
        if quantiles_str:
            quantiles = quantiles_str.split(",")
            for i in range(len(quantiles)):
                try:
                    quantiles[i] = float(quantiles[i])
                except ValueError as e:
                    logger.error("parse_quantiles_from_string ValueError", e)
        logger.debug(f"quantiles: {quantiles} ")
        return quantiles

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
