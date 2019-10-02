#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:06:47 2019

@author: usrivastava
@description:
    This is an instance of vector and corresponding classifier model, with appropriate functions
    This instance can be pickled/ unpicked
"""

import numpy as np
import configparser
import logging
import json

# Setup Logging
from modules.utils import utility_functions

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup reading from config
config = configparser.ConfigParser()
config.read('config.ini')


class ClassifierInstance:

    def __init__(self, unique_train_df, model, vector, use_decision_function, decision_boundary):
        self.model = model
        self.vector = vector
        self.use_decision_function = use_decision_function
        self.decision_boundary = decision_boundary
        self.unique_train_df = unique_train_df

        logger.info(self.unique_train_df.head(1))

        # column names
        self.col_lang = config['mongo-data']['col_lang']
        self.col_category = config['mongo-data']['col_category']
        # derived column with label encoding
        self.col_category_numeric = self.col_category + "_numeric"
        self.col_query = config['mongo-data']['col_query']
        self.col_response = config['mongo-data']['col_response']
        self.col_variables = config['mongo-data']['col_variables']
        self.col_input_circumstance = config['mongo-data']['col_input_circumstance']
        self.col_output_circumstance = config['mongo-data']['col_output_circumstance']

    """
    @description : getter for the model class
    """

    def get_model(self):
        return self.model

    """
    @description : getter for the vector class
    """

    def get_vector(self):
        return self.vector

    """
    @description : this method extracts the relevant generic column wrt category numeric value
    
    If numeric category is >= 0, it is handled suitably
    else if numeric_category is < 0, appropriate responses are returned
    # TODO : add system generated intent for unclassifiable queries
    """

    def __extract_value_from_train_data(self, lang, numeric_category, column_name):
        logger.info("__extract_value_from_train_data__")
        logger.info(self.unique_train_df.head(1))
        if numeric_category != -1:
            df = self.unique_train_df[(self.unique_train_df[self.col_lang] == lang) &
                                      (self.unique_train_df[self.col_category_numeric] == numeric_category)]
            response = None
            if (df is not None) and (df.shape[0] == 1):
                response = df[column_name].to_numpy()[0]
            else:
                response = None

        else:

            response = None

        return response

    """
    @description : this method extracts the relevant response wrt category numeric value
    """

    def extract_response(self, lang, numeric_category):
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_response)


    """
    @description : this method will select random response from the given responses and prepare a list of responses
    """

    def get_final_response_list(self, lang, numeric_category):
        # TODO - Add this as default system intent for unclassifiable queries : issue#22
        unclassifiable_response = {
            "response": [{"text": ["I am not sure I understood", "Could you rephrase the query?",
                                   "I am sorry I cannot help with this"], "custom": ""}]
        }

        # TODO - extract response from json and send appropriate randomized response
        if numeric_category != -1:
            response_list = self.extract_response(lang, numeric_category)
            logger.info("numeric_category : {0}".format(numeric_category))
            logger.info("response_list : {0}".format(response_list))
        else:
            response_list = unclassifiable_response.get("response")

        if response_list is not None:
            try:
                logger.info("response_list type : {0}".format(type(response_list)))
                if type(response_list) == str:
                    response_list = str(response_list).replace("'", '"')
                    response_list = json.loads(response_list)
                # get response, replace ' with ", so that it is convertible to json
                logger.info("response_list : {0}".format(response_list))

                # response could be a list of responses, so we should prepare a list of filtered responses and use it
                replies = []
                for response in response_list:
                    logger.info("inside response_list array loop")
                    response = str(response).replace("'", '"')
                    logger.info("response : {0}".format(response))
                    if response is not None:
                        response_json = json.loads(response)
                    # response json text element is a list of possible responses.
                    # Use a random index to get random response
                    index = utility_functions.get_random_number(len(response_json.get("text"))-1)
                    logger.info("index value : {0}".format(index))
                    text_str = response_json.get("text")[index]
                    logger.info("text_str : {0}".format(text_str))
                    custom_json_str = response_json.get("custom")
                    logger.info("custom_json_str : {0}".format(custom_json_str))
                    reply = {
                        "text" : text_str,
                        "custom" : custom_json_str
                    }
                    replies.append(reply)

            except Exception as e:
                logger.error(e)
                reply = {
                    "text": "I think you broke me. Try after some time!",
                    "custom": ""
                }
                replies.append(reply)

            # prepare a dictionary of responses

        return replies

    """
    @description : this method extracts the relevant response wrt category numeric value
    """

    def extract_input_circumstance(self, lang, numeric_category):
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_input_circumstance)

    """
    @description : this method extracts the relevant response wrt category numeric value
    """

    def extract_output_circumstance(self, lang, numeric_category):
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_output_circumstance)

    """
    @description : this method extracts the relevant response wrt category numeric value
    """

    def extract_variables(self, lang, numeric_category):
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_variables)

    """
    @description : this is the final response returned for a prediction 
    """

    def query_response(self, lang, numeric_category):
        reaction = {
            "response": self.get_final_response_list(lang, numeric_category),
            "input_circumstance": self.extract_input_circumstance(lang, numeric_category),
            "output_circumstance": self.extract_output_circumstance(lang, numeric_category),
            "variables": self.extract_variables(lang, numeric_category)

        }
        return reaction

    """
    @description : this is used for vectorizing input data
    """

    def __vectorize_data(self, data):
        X_vect = self.vector.transform(data)
        return X_vect

    """
    @description : prediction function.
    """

    def predict(self, lang, query):
        X_pred = self.__vectorize_data([query])
        y_pred = self.model.predict(X_pred)

        """
        if the function requires a decision boundary, then use the given boundary, else let prediction return a reaction
        """
        if self.use_decision_function:
            logger.info("decision_function : {0}".format(np.amax(self.model.decision_function(X_pred))))
            logger.info("decision_boundary : {0}".format(self.decision_boundary))
            if np.amax(self.model.decision_function(X_pred)) < self.decision_boundary:
                numeric_category = -1
                # At this point of time, bot should save the question

            else:
                numeric_category = y_pred[0]
        else:
            numeric_category = y_pred[0]

        response = self.query_response(lang, numeric_category)

        return response

    def predict_category(self, lang, query):
        X_pred = self.__vectorize_data([query])
        y_pred = self.model.predict(X_pred)

        """
        if the function requires a decision boundary, then use the given boundary, else let prediction return a reaction
        """
        if self.use_decision_function:
            if np.amax(self.model.decision_function(X_pred)) < self.decision_boundary:
                numeric_category = -1
                response = numeric_category
                # At this point of time, bot should save the question

            else:
                response = y_pred[0]
        else:
            response = y_pred[0]

        return response
