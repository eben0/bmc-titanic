from typing import Union

from datasource.titanic_ds_db import TitanicDatasourceDb
from datasource.titanic_ds_csv import TitanicDatasourceCSV
from lib.config import Config


# class that handles different datasource's
class Datasource:
    DB = "db"
    CSV = "csv"

    def __init__(self):
        self.config = Config.instance().all()
        self.data_source = self.config.get("dataSource", Datasource.DB)

    def __map(self):
        return {
            Datasource.DB: TitanicDatasourceDb,
            Datasource.CSV: TitanicDatasourceCSV,
        }

    def __load(self) -> Union[TitanicDatasourceDb]:
        ds_map = self.__map()
        data_source = self.data_source
        if self.data_source not in ds_map:
            data_source = Datasource.DB
        return ds_map[data_source]()

    @staticmethod
    def load():
        return Datasource().__load()
