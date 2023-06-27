import pandas as pd
from logger import logging
from exception import CustomException
from dataclasses import dataclass
import os
import sys


@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifacts', "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            # loading dataset from cvs for now(update this to load data from API and save the dataframe in sql)
            df = pd.read_csv('notebook\data\churndata.csv')
            df.to_csv(self.ingestion_config.raw_data_path,
                      index=False, header=True)
            return

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
