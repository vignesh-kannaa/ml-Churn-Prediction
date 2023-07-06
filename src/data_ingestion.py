import pandas as pd
from logger import logging
from exception import CustomException
from dataclasses import dataclass
import os
import sys

from db_connection import DBData


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('notebook/data', "churndata.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            result, column_names = DBData.get_finance_data()
            df = pd.DataFrame(result, columns=column_names)
            df.to_csv(self.ingestion_config.raw_data_path,
                      index=False, header=True)
            return

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
