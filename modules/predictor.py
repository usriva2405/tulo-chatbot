'''
Created on Sun Sep 15 10:56:19 2019

@author: usrivastava
@description:
    generic predictor class wrapper with all implementations.
    
    TODO: Improve predict function implementation
'''
# -*- coding: utf-8 -*-
import time
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, classification_report

# custom modules/ packages
from modules.nlp_query_parser import vectorizer_factory
from modules.nlp_query_parser.vector_type import VectorType
from modules.nlp_query_parser.model_selection import model_factory
from modules.model_wrapper.classifier_instance import ClassifierInstance

import configparser

import warnings

warnings.filterwarnings('ignore')

config = configparser.ConfigParser()
config.read('config.ini')


class Predictor:
    """
    This function defines the columns for prediction
    This also defines the language dictionary to be used for prediction models.
    """

    def __init__(self, vector_type, model_type, train_file_location):
        # training file location
        self.train_file_location = train_file_location

        # language column to be used for dictionary of predictors
        self.col_lang = config['mongo-data']['col_lang']

        # dependent columns
        self.col_query = config['mongo-data']['col_query']

        # target columns
        self.col_category = config['mongo-data']['col_category']

        # derived column with label encoding
        self.col_category_numeric = self.col_category + "_numeric"

        # Corresponding columns which will be extracted from predicted category
        self.col_response = config['mongo-data']['col_response']
        self.col_variables = config['mongo-data']['col_variables']
        self.col_input_circumstance = config['mongo-data']['col_input_circumstance']
        self.col_output_circumstance = config['mongo-data']['col_output_circumstance']

        # additional data about model and vector
        self.model_type = model_type
        self.model_category = model_factory.get_model(model_type)
        self.model = None
        self.vector_type = vector_type
        self.vector = vectorizer_factory.get_vector(vector_type)

        self.train_df = None
        self.unique_train_df = None
        self.X_train = None
        self.X_train_vect = None
        self.X_test = None
        self.X_test_vect = None
        self.y_train = None
        self.y_test = None

    """
    @description : this method is used for setting up the training data.
    call all relevant methods which require to be pipelined in this method.
    """

    def setup_train_data(self):
        self.__read_train_data()
        self.train_df = self.preprocess_data(self.train_df)
        self.train_df = self.encode_target_label(self.train_df, self.col_category, self.col_category_numeric)
        self.__define_unique_df()

    def __read_train_data(self):
        self.train_df = pd.read_csv(self.train_file_location)
        return self.train_df

    """
    @description : this method creates a unique classification set, which can be used later.
    """

    def __define_unique_df(self):
        self.unique_train_df = self.train_df.drop(columns=[self.col_query], axis=1).drop_duplicates()

    """
    @description : This prepares the training and test split
    """

    def __split_data(self):
        X = self.train_df[self.col_query].values
        y = self.train_df[self.col_category_numeric].values
        print('split_data')
        print('unique values for {0}'.format(self.col_category_numeric))
        print(np.unique(self.train_df[self.col_category_numeric].values))

        # split the new DataFrame into training and testing sets [Default test size = 25%]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, random_state=1)

        return self.X_train, self.X_test, self.y_train, self.y_test

    """
    @description : This is to vectorize the training data and validation data
    :return: X_train_vect, y_train, X_test_vect, y_test
    """

    def __vectorize_train_test(self):
        self.__split_data()

        self.vector = vectorizer_factory.get_vector(self.vector_type)
        self.X_train_vect = self.vector.fit_transform(self.X_train)
        self.X_test_vect = self.vector.transform(self.X_test)
        return self.X_train_vect, self.y_train, self.X_test_vect, self.y_test

    # For accurate scoring
    def __get_score(self, predictions, labels):
        print('R2: {}'.format(r2_score(labels, predictions)))
        print('RMSE: {}'.format(np.sqrt(mean_squared_error(labels, predictions))))
        cr = classification_report(labels, predictions)
        print(cr)

    def __get_start_time(self):
        return time.time()

    def __print_execution_time(self, start_time, function_str):
        end_time = time.time()
        print("Execution of " + function_str + " function took " + str(end_time - start_time) + " seconds")

    """
    @description : private method to fetch instance of classifier
    """

    def __get_classifier_instance(self, use_decision_function, decision_boundary):
        return ClassifierInstance(self.unique_train_df, self.model, self.vector, use_decision_function,
                                  decision_boundary)

    """
    @description : this method is used for preprocessing the data. incase if no preprocessing is required, ignore it.

    Reason it does not deal with class variables and instead works with instance variables is to improve flexibility.
    """

    def preprocess_data(self, data):
        return data

    """
    @description : this method encodes the target variable category.

    Reason it does not deal with class variables and instead works with instance variables is to improve flexibility.
    """

    def encode_target_label(self, data, column_name, column_name_numeric):
        labelEncoder = LabelEncoder()
        data[column_name_numeric] = labelEncoder.fit_transform(data[column_name])
        return data

    """
    @description : this method is ultimately called for fitting the model on training data
    """
    def fit_train_test(self, use_decision_function, decision_boundary):
        print('--------------------------------------------------------------------------------')
        self.model = model_factory.get_model(self.model_type)
        print('train for answers')
        # answers
        self.__vectorize_train_test()
        start_time = self.__get_start_time()
        self.model.fit(self.X_train_vect, self.y_train)

        self.__print_execution_time(start_time, "fit on train")

        start_time = self.__get_start_time()
        y_pred_train_ans = self.model.predict(self.X_train_vect)
        self.__print_execution_time(start_time, "predict on train")

        # Printing model
        print(self.model)
        # Printing train scores
        start_time = self.__get_start_time()
        self.__get_score(y_pred_train_ans, self.y_train)
        self.__print_execution_time(start_time, "get_score on train")

        start_time = self.__get_start_time()
        y_pred_test_ans = self.model.predict(self.X_test_vect)
        self.__print_execution_time(start_time, "predict on test")

        # Printing test scores
        print("Test score")
        start_time = self.__get_start_time()
        self.__get_score(y_pred_test_ans, self.y_test)
        self.__print_execution_time(start_time, "get_score on test")

        # Average R2 score and standart deviation of 5-fold cross-validation
        start_time = self.__get_start_time()
        scores = cross_val_score(self.model, self.X_test_vect, self.y_test, cv=5)
        self.__print_execution_time(start_time, "cross_val_score on test")
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

        return self.__get_classifier_instance(use_decision_function, decision_boundary)
