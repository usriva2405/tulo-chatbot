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
col_answers_str = 'answer'
col_answers_ordinal = 'answer-type'
col_ques_str = 'question'

predictor = Predictor(VectorType.TFIDF, ModelType.LOGISTIC, train_file_location, col_answers_str, col_answers_ordinal, col_ques_str)

data = predictor.read_train_data()
data = predictor.preprocess_data(data)
predictor.generate_response_dictionary(data)

X_train_vect, y_train, X_test_vect, y_test = predictor.vectorize_train_test(data)

model = predictor.train_model(X_train_vect, y_train)

predictor.fit_train_test(data)

#save the model
filename = 'saved_models/TFIDF_LOGISTIC_01_BANK_APP.sav'
pickle.dump(predictor, open(filename, 'wb'))