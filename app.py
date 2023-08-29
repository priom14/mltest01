from src.mlproject.logger import logging
from src.mlproject.exception import CustomExpection
import sys


if __name__ == "__main__":
    logging.info("The execution has startded!")
    
    try: 
        a = 1/0
    except Exception as e:
        logging.info("Custom Expection")
        raise CustomExpection(e,sys)