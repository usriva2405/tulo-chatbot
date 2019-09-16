#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 15:06:47 2019

@author: usrivastava
@description:
    This is an instance of vector and corresponding classifier model, with appropriate functions
    This instance can be pickled/ unpicked
"""

import numpy as np

class ClassifierInstance:
    
    def __init__(self, model, vector, target_dictionary):
        self.model = model
        self.vector = vector
        self.target_dictionary = target_dictionary
        
    def get_model(self):
        return self.model
    
    def get_vector(self):
        return self.vector
    
    def vectorize_data(self, data):
        X_vect = self.vector.transform(data)
        return X_vect


    def predict(self, X_str):
        print('query received by ClassifierInstance')
        X_pred = self.vectorize_data([X_str])
        y_pred = self.model.predict(X_pred)
        print(self.model.decision_function(X_pred))
        print("predicted value is - {0}".format(y_pred[0]))
        for (i, confidence) in zip (range(0,22), self.model.decision_function(X_pred)[0]):
            print("confidence for {0}:{1} is {2}".format(i, self.target_dictionary.get(i), confidence))
        print(self.model.decision_function(X_pred))
        if np.amax(self.model.decision_function(X_pred)) < 0.03 :
            response = "I'm not sure I understood your question"
            # At this point of time, bot should save the question
            
        else:
            response = self.target_dictionary.get(y_pred[0])
        
        return response