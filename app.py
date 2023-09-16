from src.mlproject.logger import logging
from src.mlproject.exception import CustomExpection
from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.components.data_ingestion import DataIngestionConfig
from src.mlproject.components.data_transformation import DataTrasformer
from src.mlproject.components.data_transformation import DataTransformationConfig
import sys


if __name__ == "__main__":
    logging.info("The execution has startded!")
    
    try: 
        # data_ingestion_path = DataIngestionConfig()
        data_ingestion = DataIngestion()
        train_path, test_path = data_ingestion.initiate_data_ingestion()
        
        data_transformer = DataTrasformer()
        data_transformer.initiate_data_tranformation(train_path,test_path)
        
    except Exception as e:
        logging.info("Custom Expection")
        raise CustomExpection(e,sys)