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
from nlp_query_parser import vectorizer_factory
from nlp_query_parser.vector_type import VectorType
from nlp_query_parser.model_selection import model_factory
from model_wrapper.classifier_instance import ClassifierInstance

import warnings
warnings.filterwarnings('ignore')

class Predictor:
    #class variables
    #train_file_location = ''
    #col_questions = ''
    #col_answers_numeric = ''
    #col_answers_str = ''
    #model = None
    #vector = None
    #response_dictionary = None
    
    def __init__(self, vector_type, model_type, train_file_location, col_answers_str, col_answers_category_str, col_ques_str, col_ques_category_str):
        self.train_file_location = train_file_location
        self.col_answers = col_answers_str
        self.col_answers_numeric = self.col_answers + "_numeric"
        self.col_questions = col_ques_str
        
        #additional columns
        self.col_answers_category = col_answers_category_str
        self.col_answers_category_numeric = self.col_answers_category + "_numeric"

        self.col_questions_category = col_ques_category_str
        self.col_questions_category_numeric = self.col_questions_category + "_numeric"

        self.model = model_factory.get_model(model_type)
        self.vector = vectorizer_factory.get_vector(vector_type)
        
    def read_train_data(self):    
        consumer_ques = pd.read_csv(self.train_file_location)
        return consumer_ques

    def preprocess_data(self, data):
        return data

    def encode_label(self, data, column_name, column_name_numeric):
        labelEncoder = LabelEncoder()
        data[column_name_numeric] = labelEncoder.fit_transform(data[column_name])
        return data

    def generate_category_dictionary(self, data, column_name, column_name_numeric):
        #response_dict = pd.Series(data['answer'],index=data['answer-type']).to_dict()
        response_dict =dict(zip(data[column_name_numeric], data[column_name]))
        print(response_dict)
        return response_dict
        #return response_dict

    def generate_response_dictionary(self, data):
        print('generating reponse dictionary')
        data = self.encode_label(data, self.col_answers, self.col_answers_numeric)
        self.response_dictionary = self.generate_category_dictionary(data, self.col_answers, self.col_answers_numeric)
        return self.response_dictionary

    def generate_ques_category_dictionary(self, data):
        print('generating questions category dictionary')
        data = self.encode_label(data, self.col_questions_category, self.col_questions_category_numeric)
        self.ques_category_dictionary = self.generate_category_dictionary(data, self.col_questions_category, self.col_questions_category_numeric)
        return self.ques_category_dictionary

    def generate_response_category_dictionary(self, data):
        print('generating response category dictionary')
        data = self.encode_label(data, self.col_answers_category, self.col_answers_category_numeric)
        self.response_category_dictionary = self.generate_category_dictionary(data, self.col_answers_category, self.col_answers_category_numeric)
        return self.response_category_dictionary

    def split_data(self, data, col_questions, col_target_numeric):
        
        X = data[col_questions].values
        y = data[col_target_numeric].values
    
        # split the new DataFrame into training and testing sets [Default test size = 25%]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        return X_train, X_test, y_train, y_test


    def vectorize_train_test(self, data, col_questions, col_target_numeric):
        X_train, X_test, y_train, y_test = self.split_data(data, col_questions, col_target_numeric)
        #vect = vectorizer_factory.get_vector(vector_type)
        X_train_vect = self.vector.fit_transform(X_train)
        X_test_vect = self.vector.transform(X_test)
        return X_train_vect, y_train, X_test_vect, y_test


    # For accurate scoring
    def get_score(self, predictions, labels):    
        print('R2: {}'.format(r2_score(labels, predictions)))
        print('RMSE: {}'.format(np.sqrt(mean_squared_error(labels, predictions))))
        cr = classification_report(labels, predictions)
        print(cr)
    
    
    def get_start_time(self):
        return time.time()

    def print_execution_time(self, start_time, function_str):
        end_time = time.time()
        print("Execution of " + function_str + " function took " + str(end_time - start_time) + " seconds")

    
    def fit_train_test(self, data, col_questions, col_target_numeric, target_dictionary):
        print('--------------------------------------------------------------------------------')
        
        X_train, y_train, X_test, y_test = self.vectorize_train_test(data, col_questions, col_target_numeric)
        start_time = self.get_start_time()
        self.model.fit(X_train, y_train)
        self.print_execution_time(start_time, "fit on train")
          
        start_time = self.get_start_time()
        y_pred_train = self.model.predict(X_train)
        self.print_execution_time(start_time, "predict on train")
        
        # Printing model
        print(self.model)
        # Printing train scores
        start_time = self.get_start_time()
        self.get_score(y_pred_train, y_train)
        self.print_execution_time(start_time, "get_score on train")
        
        start_time = self.get_start_time()
        y_pred_test = self.model.predict(X_test)
        self.print_execution_time(start_time, "predict on test")
        
        # Printing test scores
        print("Test score")
        start_time = self.get_start_time()
        self.get_score(y_pred_test, y_test)
        self.print_execution_time(start_time, "get_score on test")
        
        # Average R2 score and standart deviation of 5-fold cross-validation
        start_time = self.get_start_time()
        scores = cross_val_score(self.model, X_test, y_test, cv=5)
        self.print_execution_time(start_time, "cross_val_score on test")
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        
        return ClassifierInstance(self.model, self.vector, target_dictionary)


    def classifier_instance(self, target_dictionary):
        return ClassifierInstance(self.model, self.vector, target_dictionary)
