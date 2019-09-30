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
            "response": [{"text": ["I'm not sure I understood", "Could you rephrase the query?",
                                   "I'm sorry I cannot help with this"], "custom": ""}]
        }

        # TODO - extract response from json and send appropriate randomized response
        if numeric_category != -1:
            response = self.extract_response(lang, numeric_category)
        else:
            response = self.extract_response(lang, numeric_category)

        return response

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
            if np.amax(self.model.decision_function(X_pred)) < self.decision_boundary:
                numeric_category = -1
                response = "I'm not sure I understood your question"
                # At this point of time, bot should save the question

            else:
                response = self.query_response(lang, y_pred[0])
        else:
            response = self.query_response(lang, y_pred[0])

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
                response = "I'm not sure I understood your question"
                # At this point of time, bot should save the question

            else:
                response = y_pred[0]
        else:
            response = y_pred[0]

        return response
