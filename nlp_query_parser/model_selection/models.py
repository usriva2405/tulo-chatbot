#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:24:03 2019

@author: usrivastava
"""
from sklearn.linear_model import LogisticRegression
#import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
# IMPORT ANN HERE
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier


class Logistic:
    def __init__(self):
        self.solver='lbfgs'
        self.max_iter=1000
        self.C=0.1
        self.multi_class='multinomial'
        self.class_weight='balanced'
    def get_model(self):
        clf = LogisticRegression(solver=self.solver , max_iter=self.max_iter, C=self.C , multi_class=self.multi_class, class_weight=self.class_weight)
        return clf
    
class RandomForest:
    def __init__(self):
        self.n_estimators=100
        self.criterion='entropy'
        self.oob_score=True
        self.class_weight='balanced'
        self.random_state=1
    def get_model(self):
        clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion, oob_score=self.oob_score, class_weight=self.class_weight, random_state=self.random_state)
        return clf
    
class ExtraTrees:
    def __init__(self):
        self.n_estimators = 1000
        self.criterion='entropy'
        self.max_features='auto'
        self.min_samples_split=2
        self.bootstrap=True
        self.oob_score=True 
    
    def get_model(self):
        clf = ExtraTreesClassifier(n_estimators = self.n_estimators, criterion=self.criterion, max_features=self.max_features, min_samples_split=self.min_samples_split, bootstrap=self.bootstrap, oob_score=self.oob_score)
        return clf
    
class Gauss:
    def __init__(self):
        self.n_estimators = 100
        
    def get_model(self):
        clf = GaussianNB()
        return clf
    
    
    
        
        
        
        