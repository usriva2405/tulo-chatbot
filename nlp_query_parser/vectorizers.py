#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:21:00 2019

@author: usrivastava
"""

import pandas as pd
import numpy as np
import scipy as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

class TfidfVector:
    
    def __init__(self, ngram_range, stop_words):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
    
    def get_vector(self):
        vector = TfidfVectorizer(self.ngram_range, self.stop_words)
        return vector
    
    
class CountVector:
    
    def __init__(self, ngram_range, stop_words):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
    
    def get_vector(self):
        vector = CountVectorizer(self.ngram_range, self.stop_words)
        return vector
    