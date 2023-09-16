import sys
import os
from src.mlproject.exception import CustomExpection
from src.mlproject.logger import logging
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

import pickle


load_dotenv()


host = os.getenv('host')
port = os.getenv('port')
user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')
collection = os.getenv('collection')



def read_sql_data():
    logging.info("Reading MongoDB database started.")
    
    
    try:
        client = MongoClient(f"{host}://{user}:{password}@{port}/")
        mydb = client.get_database(db)
        logging.info("Connection Established",mydb)
        data = mydb.get_collection(collection)
        
        cursor = data.find()
        
        df = pd.DataFrame(list(cursor))
        
        print(df.head())
        
        return df
    
    except Exception as e:
        raise CustomExpection(e,sys)
    

def save_object(file_path,obj):
    try: 
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj,file_obj)
        
    
    except Exception as e:
        raise CustomExpection(e,sys)
    