#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:43:27 2019

@author: usrivastava
"""

from modules.nlp_query_parser.model_selection.models import Logistic, RandomForest, ExtraTrees, Gauss, SVM
from modules.nlp_query_parser.model_selection.model_type import ModelType

def get_model(type):
    if type == ModelType.LOGISTIC:
        return Logistic().get_model()
    elif type == ModelType.XG_BOOST:
        return None
    elif type == ModelType.RANDOM_FOREST:
        return RandomForest().get_model()
    elif type == ModelType.EXTRA_TREE:
        return ExtraTrees().get_model()
    elif type == ModelType.SVC:
        return SVM().get_model()
    elif type == ModelType.NB:
        return Gauss().get_model()
    elif type == ModelType.ANN:
        return None
    elif type == ModelType.BAGGING:
        return None
    elif type == ModelType.KNN:
        return None