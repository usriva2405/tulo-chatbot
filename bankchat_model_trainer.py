#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 10:56:19 2019

@author: usrivastava
@description:
    run/ Use this separately to train the model for bank chat.
    everytime model is updated/ changed, this should be re-run.
    
    TODO: improve the structure of this trainer, to make it more dynamic
    
    To change model:
        change enum Modeltype.LOGISTIC to desired model
    To change vectorizer:
        change enum VectorType.TFIDF to desired vector implementation
        
    RECOMMENDATION: change the filename when you change the model
"""

from response_predictor import Predictor
from nlp_query_parser.vector_type import VectorType
from nlp_query_parser.model_selection.model_type import ModelType
import pickle


train_file_location = 'consumer_questions.csv'

#dependent columns
col_questions = 'question'

#target columns
col_answers = 'answer'
col_answers_category = 'answer-category'
col_questions_category = 'question-category'

#equivalent numeric columns
col_answers_numeric = col_answers + "_numeric"
col_answers_category_numeric = col_answers_category + "_numeric"
col_questions_category_numeric = col_questions_category + "_numeric"

predictor = Predictor(VectorType.TFIDF, ModelType.SVC, train_file_location, col_answers, col_answers_category, col_questions, col_questions_category)

data = predictor.read_train_data()
data = predictor.preprocess_data(data)
response_dictionary = predictor.generate_response_dictionary(data)
ques_category_dictionary = predictor.generate_ques_category_dictionary(data)
response_category_dictionary = predictor.generate_response_category_dictionary(data)

X_train_vect, y_train, X_test_vect, y_test = predictor.vectorize_train_test(data, col_questions, col_answers_numeric)

answers_classifier = predictor.fit_train_test(data, col_questions, col_answers_numeric, response_dictionary)
ques_category_classifier = predictor.fit_train_test(data, col_questions, col_questions_category_numeric, ques_category_dictionary)
answers_category_dictionary = predictor.fit_train_test(data, col_questions, col_answers_category_numeric, response_category_dictionary)

#save the model
filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS.sav'
pickle.dump(answers_classifier, open(filename, 'wb'))

filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS_CATEGORY.sav'
pickle.dump(answers_category_dictionary, open(filename, 'wb'))

filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_QUESTIONS_CATEGORY.sav'
pickle.dump(ques_category_classifier, open(filename, 'wb'))