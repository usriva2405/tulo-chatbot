#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:23:01 2019

@author: usrivastava
"""

from nlp_query_parser.vectorizers import TfidfVector, CountVector
from nlp_query_parser.vector_type import VectorType

def get_vector(type):
    if type == VectorType.TFIDF:
        return TfidfVector(ngram_range=(1,3), stop_words="english").get_vector()
    elif type == VectorType.COUNT:
        return CountVector(ngram_range=(1,3), stop_words="english").get_vector()
