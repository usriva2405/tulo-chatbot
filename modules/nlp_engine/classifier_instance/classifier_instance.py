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
import json

# Setup Logging
from modules.utils import utility_functions
from modules.utils.yaml_parser import Config
from modules.utils.app_logger import AppLogger

logger = AppLogger()


class ClassifierInstance:

    def __init__(self, unique_train_df, model, vector, use_decision_function, decision_boundary):
        """
        constructor to initialize class params

        :param unique_train_df: unique classes
        :param model: model used for training
        :param vector: vectorizer used for training
        :param use_decision_function: whether to use decision function or not
        :param decision_boundary: threshold for decision function
        """
        self.model = model
        self.vector = vector
        self.use_decision_function = use_decision_function
        self.decision_boundary = decision_boundary
        self.unique_train_df = unique_train_df

        logger.info(self.unique_train_df.head(1))

        # column names
        self.col_lang = Config.get_config_val(key="df_columns", key_1depth="col_lang")
        self.col_category = Config.get_config_val(key="df_columns", key_1depth="col_category")
        # derived column with label encoding
        self.col_category_numeric = self.col_category + "_numeric"
        self.col_query = Config.get_config_val(key="df_columns", key_1depth="col_query")
        self.col_response = Config.get_config_val(key="df_columns", key_1depth="col_response")
        self.col_variables = Config.get_config_val(key="df_columns", key_1depth="col_variables")
        self.col_input_circumstance = Config.get_config_val(key="df_columns", key_1depth="col_input_circumstance")
        self.col_output_circumstance = Config.get_config_val(key="df_columns", key_1depth="col_output_circumstance")

    def get_model(self):
        """
        getter for the model class
        :return:
        """
        return self.model

    def get_vector(self):
        """
        getter for the vector class
        :return:
        """
        return self.vector

    def __extract_value_from_train_data(self, lang, numeric_category, column_name):
        """
        This method extracts the relevant generic column wrt category numeric value

        If numeric category is >= 0, it is handled suitably
        else if numeric_category is < 0, appropriate responses are returned
        # TODO : add system generated intent for unclassifiable queries

        :param lang: language used for classification
        :param numeric_category: predicted category
        :param column_name: column to be extracted
        :return: extracted value for given column
        """
        logger.info("__extract_value_from_train_data__")
        logger.info(self.unique_train_df[self.col_category_numeric].value_counts())
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

    def extract_response(self, lang, numeric_category):
        """
        This method extracts the relevant response wrt category numeric value
        :param lang:
        :param numeric_category:
        :return:
        """
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_response)

    def get_final_response_list(self, lang, numeric_category):
        """
        This method will select random response from the given responses and prepare a list of responses
        :param lang:
        :param numeric_category:
        :return:
        """
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

        # the only condition response list would be null would be in case the language isn't supported

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
                    index = utility_functions.get_random_number(len(response_json.get("text")) - 1)
                    logger.info("index value : {0}".format(index))
                    text_str = response_json.get("text")[index]
                    logger.info("text_str : {0}".format(text_str))
                    custom_json_str = response_json.get("custom")
                    logger.info("custom_json_str : {0}".format(custom_json_str))
                    reply = {
                        "text": text_str,
                        "custom": custom_json_str
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

    def extract_input_circumstance(self, lang, numeric_category):
        """
        This method extracts the relevant response wrt category numeric value
        :param lang:
        :param numeric_category:
        :return:
        """
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_input_circumstance)

    def extract_output_circumstance(self, lang, numeric_category):
        """
        This method extracts the relevant response wrt category numeric value
        :param lang:
        :param numeric_category:
        :return:
        """
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_output_circumstance)

    def extract_variables(self, lang, numeric_category):
        """
        This method extracts the relevant response wrt category numeric value
        :param lang:
        :param numeric_category:
        :return:
        """
        return self.__extract_value_from_train_data(lang, numeric_category, self.col_variables)

    def query_response(self, lang, numeric_category):
        """
        This is the final response returned for a prediction
        :param lang:
        :param numeric_category:
        :return:
        """
        reaction = {
            "response": self.get_final_response_list(lang, numeric_category),
            "input_circumstance": self.extract_input_circumstance(lang, numeric_category),
            "output_circumstance": self.extract_output_circumstance(lang, numeric_category),
            "variables": self.extract_variables(lang, numeric_category)

        }
        return reaction

    def __vectorize_data(self, data):
        """
        This is used for vectorizing input data
        :param data:
        :return:
        """
        X_vect = self.vector.transform(data)
        return X_vect

    def predict(self, lang, query):
        """
        prediction function.
        :param lang:
        :param query:
        :return:
        """
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
        """
        Only returns the predicted category
        :param lang:
        :param query:
        :return:
        """
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
