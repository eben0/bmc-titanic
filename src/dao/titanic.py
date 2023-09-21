import logging
from typing import List, Dict

from dao.schema import titanic_schema
from datasource.datasource import Datasource
from lib.config import Config

DEFAULT_QUANTILES = [
    0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4,
    0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
    0.85, 0.9, 0.95, 1
]
DEFAULT_LIMIT = 100

logger = logging.getLogger()


class Titanic:
    def __init__(self):
        self.config = Config.instance().all()
        self.data_source = Datasource.load()

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
        limit = self.get_limit(request.args.get("limit"))
        try:
            return self.data_source.get_passengers(id, cols, limit)
        except Exception as e:
            logger.error("Unable to get passengers from datasource", e)
            raise e

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
        # create the list
        for q in qs:
            results.append({"y": quantiles[i] * 100, "x": q})
            i += 1

        logger.debug(f"prices_quantile result {results}")
        return results

    def get_prices_dataframe(self):
        """
        gets the proces as pandas dataframe
        :return: dataframe of prices
        """
        try:
            # gets the datasource
            return self.data_source.get_prices()
        except Exception as e:
            logger.error("Unable to load records from datasource", e)
            raise e

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

    def get_limit(self, limit=DEFAULT_LIMIT):
        """
        gets and normalizes the limit value
        :param limit: limit
        :return: limit
        """
        try:
            if limit is None:
                return DEFAULT_LIMIT
            return int(limit)
        except ValueError:
            return DEFAULT_LIMIT
