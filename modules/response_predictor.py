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

        self.model_type = model_type
        self.model_ans = model_factory.get_model(model_type)
        self.vector_type = vector_type
        self.vector = vectorizer_factory.get_vector(vector_type)
        
        # not getting used anymore
        self.model_ans_cat = model_factory.get_model(model_type)
        self.model_ques_cat = model_factory.get_model(model_type)
        
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
        return response_dict
        #return response_dict

    def generate_response_dictionary(self, data):
        data = self.encode_label(data, self.col_answers, self.col_answers_numeric)
        self.response_dictionary = self.generate_category_dictionary(data, self.col_answers, self.col_answers_numeric)
        return self.response_dictionary

    def generate_ques_category_dictionary(self, data):
        data = self.encode_label(data, self.col_questions_category, self.col_questions_category_numeric)
        self.ques_category_dictionary = self.generate_category_dictionary(data, self.col_questions_category, self.col_questions_category_numeric)
        return self.ques_category_dictionary

    def generate_response_category_dictionary(self, data):
        data = self.encode_label(data, self.col_answers_category, self.col_answers_category_numeric)
        self.response_category_dictionary = self.generate_category_dictionary(data, self.col_answers_category, self.col_answers_category_numeric)
        return self.response_category_dictionary

    def split_data(self, data, col_questions, col_target_numeric):
        
        X = data[col_questions].values
        y = data[col_target_numeric].values
        print('split_data')
        print('unique values for {0}'.format(col_target_numeric))
        print(np.unique(data[col_target_numeric].values))
        
        # split the new DataFrame into training and testing sets [Default test size = 25%]
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
        
        return X_train, X_test, y_train, y_test


    def vectorize_train_test(self, data, col_questions, col_target_numeric):
        X_train, X_test, y_train, y_test = self.split_data(data, col_questions, col_target_numeric)
        
        self.vector = vectorizer_factory.get_vector(self.vector_type)
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

    
    def fit_train_test(self, data, ques_col, target_col_numeric, target_dictionary, use_decision_function, decision_boundary):
        print('--------------------------------------------------------------------------------')
        self.model_ans = model_factory.get_model(self.model_type)
        print('train for answers')
        #answers
        X_train_ans, y_train_ans, X_test_ans, y_test_ans = self.vectorize_train_test(data, ques_col, target_col_numeric)
        start_time = self.get_start_time()
        self.model_ans.fit(X_train_ans, y_train_ans)

        '''
        print('train for answers categories')
        #answers categories
        X_train_ans_cat, y_train_ans_cat, X_test_ans_cat, y_test_ans_cat = self.vectorize_train_test(data, self.col_questions, self.col_answers_category_numeric)
        start_time = self.get_start_time()
        self.model_ans_cat.fit(X_train_ans_cat, y_train_ans_cat)

        print('train for question categories')
        #question categories
        X_train_ques_cat, y_train_ques_cat, X_test_ques_cat, y_test_ques_cat = self.vectorize_train_test(data, self.col_questions, self.col_questions_category_numeric)
        start_time = self.get_start_time()
        self.model_ques_cat.fit(X_train_ques_cat, y_train_ques_cat)
        '''

        self.print_execution_time(start_time, "fit on train")
          
        start_time = self.get_start_time()
        y_pred_train_ans = self.model_ans.predict(X_train_ans)
        self.print_execution_time(start_time, "predict on train")
        
        # Printing model
        print(self.model_ans)
        # Printing train scores
        start_time = self.get_start_time()
        self.get_score(y_pred_train_ans, y_train_ans)
        self.print_execution_time(start_time, "get_score on train")
        
        start_time = self.get_start_time()
        y_pred_test_ans = self.model_ans.predict(X_test_ans)
        self.print_execution_time(start_time, "predict on test")
        
        # Printing test scores
        print("Test score")
        start_time = self.get_start_time()
        self.get_score(y_pred_test_ans, y_test_ans)
        self.print_execution_time(start_time, "get_score on test")
        
        # Average R2 score and standart deviation of 5-fold cross-validation
        start_time = self.get_start_time()
        scores = cross_val_score(self.model_ans, X_test_ans, y_test_ans, cv=5)
        self.print_execution_time(start_time, "cross_val_score on test")
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        
        return self.get_classifier_instance(target_dictionary, use_decision_function, decision_boundary)
    
    
    def get_classifier_instance(self, target_dictionary, use_decision_function, decision_boundary):
        return ClassifierInstance(self.model_ans, self.vector, target_dictionary, use_decision_function, decision_boundary) 
        
    
    def vectorize_data(self, X_str):
        return self.vector.transform([X_str])


    def predict(self, X_str):
        print('query received by ClassifierInstance')
        X_pred = self.vectorize_data(X_str)
        print("-------------")
        print(self.vector.get_feature_names())
        print(X_pred.shape)
        
        #answer prediction
        y_pred_ans = self.model_ans.predict(X_pred)
        print("predicted ans value is - {0}".format(y_pred_ans[0]))
        for (i, confidence) in zip (range(0,22), self.model_ans.decision_function(X_pred)[0]):
            print("confidence for {0}:{1} is {2}".format(i, self.response_dictionary.get(i), confidence))
        print(self.model_ans.decision_function(X_pred))
        if np.amax(self.model_ans.decision_function(X_pred)) < 0.03 :
            response = "I'm not sure I understood your question"
            # At this point of time, bot should save the question
            
        else:
            response = self.response_dictionary.get(y_pred_ans[0])
        
        '''
        #answer category prediction
        y_pred_ans_cat = self.model_ans_cat.predict(X_pred)
        print(self.model_ans_cat.decision_function(X_pred))
        print("predicted ans cat value is - {0}".format(y_pred_ans_cat[0]))
        response_cat = self.response_category_dictionary.get(y_pred_ans_cat[0])


        #question category prediction
        y_pred_ques_cat = self.model_ques_cat.predict(X_pred)
        print(self.model_ques_cat.decision_function(X_pred))
        print("predicted question cat value is - {0}".format(y_pred_ques_cat[0]))
        for (i, confidence) in zip (range(0,22), self.model_ques_cat.decision_function(X_pred)[0]):
            print("confidence for {0}:{1} is {2}".format(i, self.ques_category_dictionary.get(i), confidence))
        question_cat = self.ques_category_dictionary.get(y_pred_ques_cat[0])
        
        return response, response_cat, question_cat
        
        '''
        return response
        