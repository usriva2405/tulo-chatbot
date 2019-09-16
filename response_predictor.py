'''
Created on Sun Sep 15 10:56:19 2019

@author: usrivastava
@description:
    generic predictor class wrapper with all implementations.
    
    TODO: Improve predict function implementation
'''
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, classification_report

# custom modules/ packages
from nlp_query_parser import vectorizer_factory
from nlp_query_parser.vector_type import VectorType
from nlp_query_parser.model_selection import model_factory
import time

import warnings
warnings.filterwarnings('ignore')

class Predictor:
    #class variables
    #train_file_location = ''
    #col_questions_str = ''
    #col_answers_ordinal = ''
    #col_answers_str = ''
    #model = None
    #vector = None
    #response_dictionary = None
    
    def __init__(self, vector_type, model_type, train_file_location, col_answers_str, col_answers_ordinal, col_ques_str):
        self.train_file_location = train_file_location
        self.col_answers = col_answers_str
        self.col_answers_ordinal = col_answers_ordinal
        self.col_questions_str = col_ques_str
        self.model = model_factory.get_model(model_type)
        self.vector = vectorizer_factory.get_vector(vector_type)
        
    def read_train_data(self):    
        consumer_ques = pd.read_csv(self.train_file_location)
        return consumer_ques

    def preprocess_data(self, data):
        return data

    def generate_response_dictionary(self, data):
        #response_dict = pd.Series(data['answer'],index=data['answer-type']).to_dict()
        response_dict =dict(zip(data[self.col_answers_ordinal], data[self.col_answers]))
        print(response_dict)
        self.response_dictionary = response_dict
        #return response_dict

    def split_data(self, data):
        
        X = data[self.col_questions_str].values
        y = data[self.col_answers_ordinal].values
    
        # split the new DataFrame into training and testing sets [Default test size = 25%]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        return X_train, X_test, y_train, y_test


    def vectorize_train_test(self, data):
        X_train, X_test, y_train, y_test = self.split_data(data)
        #vect = vectorizer_factory.get_vector(vector_type)
        X_train_vect = self.vector.fit_transform(X_train)
        X_test_vect = self.vector.transform(X_test)
        return X_train_vect, y_train, X_test_vect, y_test


    def train_model(self, X_train_vec, y_train):
        #clf = model_factory.get_model(model_type)
        self.model.fit(X_train_vec, y_train)
        return self.model


    # For accurate scoring
    def get_score(self, predictions, labels):    
        print('R2: {}'.format(r2_score(labels, predictions)))
        print('RMSE: {}'.format(np.sqrt(mean_squared_error(labels, predictions))))
        cr = classification_report(labels, predictions)
        print(cr)
    
    
    
    def fit_train_test(self, data):
        X_train, y_train, X_test, y_test = self.vectorize_train_test(data)
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



    def get_start_time(self):
        return time.time()

    def print_execution_time(self, start_time, function_str):
        end_time = time.time()
        print("Execution of " + function_str + " function took " + str(end_time - start_time) + " seconds")

    def vectorize_data(self, data):
        X_vect = self.vector.transform(data)
        return X_vect


    def predict(self, X_str):
        X_pred = self.vector.transform([X_str])
        y_pred = self.model.predict(X_pred)
        #print(self.model.predict_proba(X_pred))
        for (i, confidence) in zip (range(18), self.model.decision_function(X_pred)):
            print("confidence for {0} is {1}".format(i, confidence))
        print(self.model.decision_function(X_pred))
        if np.amax(self.model.decision_function(X_pred)) < 0.09 :
            response = "I'm not sure I understood your question"
            # At this point of time, bot should save the question
            
        else:
            response = self.response_dictionary.get(y_pred[0])
        
        return response
    



