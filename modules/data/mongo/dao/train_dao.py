'''
Created on Sun Sep 22 22:26:19 2019

@author: usrivastava
@description:
    This is a dao for training data
'''

from mongoengine import *
import pandas as pd
import numpy as np
import configparser
import logging
import json
from modules.data.mongo.dao.model import Train, Response, Variables, Circumstance

#Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Setup reading from config
config = configparser.ConfigParser()
config.read('config.ini')

class TrainDao:
    def __init__(self):


        # column names
        self.col_lang = config['mongo-data']['col_lang']
        self.col_category = config['mongo-data']['col_category']
        self.col_query = config['mongo-data']['col_query']
        self.col_response = config['mongo-data']['col_response']
        self.col_variables = config['mongo-data']['col_variables']
        self.col_input_circumstance = config['mongo-data']['col_input_circumstance']
        self.col_output_circumstance = config['mongo-data']['col_output_circumstance']
        self.train_file_location = 'modules/data/' + config['mongo-data']['mongo_train_fileName']

        self.train_list = []
        self.df_train_flatfile = pd.DataFrame()
        # setup everything
        # This should not be part of the class initialization, and instead should be explicit event.
        # self.setup_flatfile()

    def setup_flatfile(self):
        self.__load_train_data()
        if self.train_list is not None:
            self.__create_flatfile()
            self.__save_flatfile()
        else:
            logger.error("data could not be loaded from mongodb")

    '''
    This will load training data from mongodb
    '''
    def __load_train_data(self):
        self.train_list = Train.objects()

    '''
    This is to create the flat file for training.
    '''
    def __create_flatfile(self):
        if (self.train_list != None) and (len(self.train_list) > 0):

            #iterate over each document in train_list
            for train_document in self.train_list:

                #check if query is not null
                if (train_document.training_queries != None) and (len(train_document.training_queries)>0):

                    row_list = []
                    #populate query
                    for query in train_document.training_queries:
                        #get response json
                        responseJson = json.loads(train_document.to_json()).get("response")
                        variablesJson = json.loads(train_document.to_json()).get("variables")

                        #create dictionary to add to df
                        row_dict = {
                            self.col_lang : train_document.lang,
                            self.col_category : train_document.category,
                            self.col_query : query,
                            self.col_response : responseJson,
                            self.col_input_circumstance : train_document.circumstance.input_circumstance,
                            self.col_output_circumstance : train_document.circumstance.output_circumstance,
                            self.col_variables : variablesJson
                        }

                        self.df_train_flatfile = self.df_train_flatfile.append(row_dict, ignore_index=True)
                else :
                    logger.info("training queries is null/ 0")

        else:
            logger.info("no data retrieved from mongodb train collection")

        return self.df_train_flatfile

    '''
    This saves the flat file to filesystem
    '''
    def __save_flatfile(self):
        self.df_train_flatfile.to_csv(self.train_file_location,index=False)


    '''
    populate mongodb with raw data
    This method reads the old format of queries, and prepares documents to append to mongoDB
    '''
    def bulk_insert_documents(self):
        #load the old file
        old_train_file_location = 'modules/data/' + config['data']['train-file-name']
        consumer_ques = pd.read_csv(old_train_file_location)

        #first change the column names
        consumer_ques.rename(columns={'question-category':config['mongodb-data']['col_category'], 'question':config['mongodb-data']['col_query'], 'answer':config['mongodb-data']['col_response']}, inplace=True)

        #in order to create 1 row per category, we will have to split data based on every category.
        #1. extract unique categories in data
        categories = consumer_ques[config['mongodb-data']['col_category']].unique()

        #2. iterate over each category
        for cat in categories:
            print('category : {0}'.format(cat))
            trainObj = None

            #3. split data per category
            df = consumer_ques[consumer_ques[config['mongodb-data']['col_category']] == cat]

            #4. extract query
            training_queries = df[[config['mongodb-data']['col_query']]].values.T.tolist()[0]

            #4.1 extract language
            lang = df['lang'].unique()[0]

            #4.2 extract category - category is already extracted in "cat"

            #5. create train object
            trainObj = Train(category=cat, lang=lang, training_queries=training_queries)

            #6. create circumstance
            circumstance = Circumstance(input_circumstance = df[config['mongodb-data']['col_input_circumstance']].unique()[0], output_circumstance = df[config['mongodb-data']['col_output_circumstance']].unique()[0])
            # circumstance = {
            #     'input_circumstance' : df['input_circumstance'].unique()[0],
            #     'output_circumstance' : df['output_circumstance'].unique()[0]
            # }

            trainObj.circumstance = circumstance

            #7. create response
            responseList = []
            textList = []
            textList.append(df[config['mongodb-data']['col_response']].unique()[0])
            response = Response(text=textList, custom = '')
            # responseObj = {
            #     'text' : textList,
            #     'custom' : ''
            # }
            # responseList.append(responseObj)
            trainObj.response.append(response)

            #8. create variables

            variables = json.loads(df[config['mongodb-data']['col_variables']].unique()[0])
            for var in variables:
                varObj = Variables(name=var.get('name'), type=var.get('type'), value=var.get('value'), io_type=var.get('io_type'))
                trainObj.variables.append(varObj)

            #9. save the object
            trainObj.save()
