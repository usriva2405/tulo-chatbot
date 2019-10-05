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
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import nltk

class TfidfVector:
    
    def __init__(self, ngram_range, stop_words):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
    
    def get_vector(self):
        vector = TfidfVectorizer(self.ngram_range, self.stop_words, tokenizer=StemmerTokenizer())
        return vector
    
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


class StemmerTokenizer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()
    def __call__(self, doc):
        tokens = [word for word in nltk.word_tokenize(doc) if len(word) > 1]
        return [self.stemmer.stem(item) for item in tokens]



class CountVector:
    
    def __init__(self, ngram_range, stop_words):
        self.ngram_range = ngram_range
        self.stop_words = stop_words
    
    def get_vector(self):
        vector = CountVectorizer(self.ngram_range, self.stop_words)
        return vector
    