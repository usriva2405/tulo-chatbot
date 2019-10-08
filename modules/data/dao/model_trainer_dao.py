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

from modules.nlp_engine.model_builder.processor import Processor
from modules.nlp_engine.vector_selection.vector_type import VectorType
from modules.nlp_engine.model_selection.model_type import ModelType
from modules.utils.yaml_parser import Config
import pickle
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def setup_model_weights():
    # training file location
    train_file_location = Config.get_config_val(key="flatfile", key_1depth="location") + Config.get_config_val(key="flatfile", key_1depth="mongo_train_fileName")

    predictor = Processor(VectorType.TFIDF, ModelType.LOGISTIC, train_file_location)

    # setup training data
    predictor.setup_train_data()
    response_classifier = predictor.fit_train_test(True, 0.18)

    # save the model
    filename = Config.get_config_val(key="model", key_1depth="file", key_2depth="location") + Config.get_config_val(key="model", key_1depth="file", key_2depth="response_classifier")
    pickle.dump(response_classifier, open(filename, 'wb'))
