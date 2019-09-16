#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:20:54 2019

@author: usrivastava
"""
from enum import Enum

class ModelType(Enum):
    LOGISTIC = 1
    XG_BOOST = 2
    RANDOM_FOREST = 3
    EXTRA_TREE = 4
    SVC = 5
    NB = 6
    ANN = 7
    BAGGING = 8
    KNN = 9
