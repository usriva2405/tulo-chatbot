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

from modules.response_predictor import Predictor
from modules.nlp_query_parser.vector_type import VectorType
from modules.nlp_query_parser.model_selection.model_type import ModelType
import pickle
import configparser
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

#training file location
train_file_location = 'modules/data/' + config['data']['train-file-name']

#dependent columns
col_questions = config['data']['ques-col']

#target columns
col_answers = config['data']['ans-col']
col_answers_category = config['data']['ans-cat-col']
col_questions_category = config['data']['ques-cat-col']

#equivalent numeric columns
col_answers_numeric = col_answers + "_numeric"
col_answers_category_numeric = col_answers_category + "_numeric"
col_questions_category_numeric = col_questions_category + "_numeric"

predictor = Predictor(VectorType.TFIDF, ModelType.LOGISTIC, train_file_location, col_answers, col_answers_category, col_questions, col_questions_category)

data = predictor.read_train_data()
data = predictor.preprocess_data(data)

# dictionaries
response_dictionary = predictor.generate_response_dictionary(data)
response_category_dictionary = predictor.generate_response_category_dictionary(data)
ques_category_dictionary = predictor.generate_ques_category_dictionary(data)


response_classifier = predictor.fit_train_test(data, col_questions, col_answers_numeric, response_dictionary, True, 0.03)
response_category_classifier = predictor.fit_train_test(data, col_questions, col_answers_category_numeric, response_category_dictionary, False, 0.0)
question_category_classifier = predictor.fit_train_test(data, col_questions, col_questions_category_numeric, ques_category_dictionary, True, 0.03)

#save the model
filename = 'modules/saved_models/' + config['model-file-name']['ans-classifier']
pickle.dump(response_classifier, open(filename, 'wb'))

filename = 'modules/saved_models/' + config['model-file-name']['ans-cat-classifier']
pickle.dump(response_category_classifier, open(filename, 'wb'))

filename = 'modules/saved_models/' + config['model-file-name']['ques-cat-classifier']
pickle.dump(question_category_classifier, open(filename, 'wb'))