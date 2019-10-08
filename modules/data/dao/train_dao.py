'''
Created on Sun Sep 22 22:26:19 2019

@author: usrivastava
@description:
    This is a dao for training data
'''

import pandas as pd
import json
from modules.data.db_model.model import Train, Response, Variables, Circumstance
from modules.utils.yaml_parser import Config
from modules.utils.app_logger import AppLogger

logger = AppLogger()


class TrainDao:
    def __init__(self):

        # column names
        self.col_lang = Config.get_config_val(key="df_columns", key_1depth="col_lang")
        self.col_category = Config.get_config_val(key="df_columns", key_1depth="col_category")
        self.col_query = Config.get_config_val(key="df_columns", key_1depth="col_query")
        self.col_response = Config.get_config_val(key="df_columns", key_1depth="col_response")
        self.col_variables = Config.get_config_val(key="df_columns", key_1depth="col_variables")
        self.col_input_circumstance = Config.get_config_val(key="df_columns", key_1depth="col_input_circumstance")
        self.col_output_circumstance = Config.get_config_val(key="df_columns", key_1depth="col_output_circumstance")
        self.train_file_location = Config.get_config_val(key="flatfile", key_1depth="location") + Config.get_config_val(key="flatfile", key_1depth="mongo_train_fileName")

        self.train_list = []
        self.df_train_flatfile = pd.DataFrame()
        # setup everything
        # This should not be part of the class initialization, and instead should be explicit event.
        # self.setup_flatfile()

    """
    This method returns dataframe, and does not save it as csv.
    #TODO add user configuration
    """
    def get_train_df(self):
        self.__load_train_data()
        if self.train_list is not None:
            self.__create_flatfile()
        else:
            logger.error("data could not be loaded from mongodb")
        return self.df_train_flatfile

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
        old_train_file_location = Config.get_config_val(key="flatfile", key_1depth="location") + Config.get_config_val(key="flatfile", key_1depth="mongo_train_fileName")
        consumer_ques = pd.read_csv(old_train_file_location)

        #first change the column names
        consumer_ques.rename(columns={'question-category':Config.get_config_val(key="df_columns", key_1depth="col_category"), 'question':Config.get_config_val(key="df_columns", key_1depth="col_query"), 'answer':Config.get_config_val(key="df_columns", key_1depth="col_response")}, inplace=True)

        #in order to create 1 row per category, we will have to split data based on every category.
        #1. extract unique categories in data
        categories = consumer_ques[Config.get_config_val(key="df_columns", key_1depth="col_category")].unique()

        #2. iterate over each category
        for cat in categories:
            print('category : {0}'.format(cat))
            trainObj = None

            #3. split data per category
            df = consumer_ques[consumer_ques[Config.get_config_val(key="df_columns", key_1depth="col_category")] == cat]

            #4. extract query
            training_queries = df[[Config.get_config_val(key="df_columns", key_1depth="col_query")]].values.T.tolist()[0]

            #4.1 extract language
            lang = df[Config.get_config_val(key="df_columns", key_1depth="col_lang")].unique()[0]

            #4.2 extract category - category is already extracted in "cat"

            #5. create train object
            trainObj = Train(category=cat, lang=lang, training_queries=training_queries)

            #6. create circumstance
            circumstance = Circumstance(input_circumstance = df[Config.get_config_val(key="df_columns", key_1depth="col_input_circumstance")].unique()[0], output_circumstance = df[Config.get_config_val(key="df_columns", key_1depth="col_output_circumstance")].unique()[0])
            # circumstance = {
            #     'input_circumstance' : df['input_circumstance'].unique()[0],
            #     'output_circumstance' : df['output_circumstance'].unique()[0]
            # }

            trainObj.circumstance = circumstance

            #7. create response
            responseList = []
            textList = []
            textList.append(df[Config.get_config_val(key="df_columns", key_1depth="col_response")].unique()[0])
            response = Response(text=textList, custom = '')
            # responseObj = {
            #     'text' : textList,
            #     'custom' : ''
            # }
            # responseList.append(responseObj)
            trainObj.response.append(response)

            #8. create variables

            variables = json.loads(df[Config.get_config_val(key="df_columns", key_1depth="col_variables")].unique()[0])
            for var in variables:
                varObj = Variables(name=var.get('name'), type=var.get('type'), value=var.get('value'), io_type=var.get('io_type'))
                trainObj.variables.append(varObj)

            #9. save the object
            trainObj.save()
