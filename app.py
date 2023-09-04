from src.mlproject.logger import logging
from src.mlproject.exception import CustomExpection
from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.components.data_ingestion import DataIngestionConfig
import sys


if __name__ == "__main__":
    logging.info("The execution has startded!")
    
    try: 
        # data_ingestion_path = DataIngestionConfig()
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()
    except Exception as e:
        logging.info("Custom Expection")
        raise CustomExpection(e,sys)