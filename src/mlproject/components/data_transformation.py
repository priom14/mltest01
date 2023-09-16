import sys
import os
import numpy as np
import pandas as pd 
from dataclasses import dataclass

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from src.mlproject.exception import CustomExpection
from src.mlproject.logger import logging
from src.mlproject.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')
    
class DataTrasformer:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        
        try:
            num_features = ['Day', 'Year', 'Month', 'Age', 'Quantity', 'Price per Unit']
            cat_features = ['Gender', 'Product Category']

            num_pipeline = Pipeline(steps=[
                ("Imputer", SimpleImputer(strategy="median")),
                ("StandardScaler", StandardScaler())
            ])
            
            cat_pipeline = Pipeline(steps=[
                ("Imputer", SimpleImputer(strategy="most_frequent")),
                ("OneHotEncoder", OneHotEncoder()),
                ("StandardScaler", StandardScaler(with_mean=False))
            ])
            
            logging.info(f"Numeircal features: {num_features}")
            logging.info(f"Categorical features: {cat_features}")
            
            
            preprocessor = ColumnTransformer(
            [
                ('Numerical', num_pipeline, num_features ),
                ('Categorical', cat_pipeline, cat_features),
            ]
            )
            
            return preprocessor
        
        
        except Exception as e :
            raise CustomExpection(e,sys)
    
    def initiate_data_tranformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("Reading the test file")
        
            preprocessor_obj = self.get_data_transformer_object()
            
            target_column = 'Total Amount'
            
            train_df['Year'] = train_df['Date'].str.split("-").str[0]
            train_df['Year'] = train_df['Year'].astype(int)
            train_df['Month'] = train_df['Date'].str.split("-").str[1]
            train_df['Month'] = train_df['Month'].astype(int)
            train_df['Day'] = train_df['Date'].str.split("-").str[2]
            train_df['Day'] = train_df['Day'].astype(int)
            
            test_df['Year'] = test_df['Date'].str.split("-").str[0]
            test_df['Year'] = test_df['Year'].astype(int)
            test_df['Month'] = test_df['Date'].str.split("-").str[1]
            test_df['Month'] = test_df['Month'].astype(int)
            test_df['Day'] = test_df['Date'].str.split("-").str[2]
            test_df['Day'] = test_df['Day'].astype(int)
            
            train_df.drop(columns='Date', inplace=True)
            test_df.drop(columns='Date', inplace=True)
            
            train_df.drop(columns=['_id','Transaction ID'], inplace= True)
            test_df.drop(columns=['_id','Transaction ID'], inplace= True)
            
            input_features_train_df = train_df.drop(columns=[target_column],axis=1)
            output_features_train_df = train_df[target_column]
            
            input_features_test_df = test_df.drop(columns=[target_column],axis=1)
            output_features_test_df = test_df[target_column]
            
            logging.info("Applying preprocerssing on the training and test dataframe")
            
            input_feature_train_arr = preprocessor_obj.fit_transform(input_features_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_features_test_df)
            
            
            train_arr = np.c_[input_feature_train_arr,np.array(output_features_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(output_features_test_df)]
            
            logging.info("Saved preprocessing object")

            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessor_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
            
        except Exception as e:
            raise CustomExpection(e,sys)