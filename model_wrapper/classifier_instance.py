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
        print(target_dictionary)
        
    def get_model(self):
        print(self.model)
        return self.model
    
    def get_vector(self):
        print(self.vector)
        return self.vector
    
    def get_dictionary(self):
        print(self.target_dictionary)
        return self.target_dictionary
    
    def vectorize_data(self, data):
        X_vect = self.vector.transform(data)
        return X_vect


    def predict(self, X_str):
        print('query received by ClassifierInstance')
        X_pred = self.vectorize_data([X_str])
        print("-------------")
        print(X_pred)
        y_pred = self.model.predict(X_pred)
        print(self.model.decision_function(X_pred))
        print("predicted value is - {0}".format(y_pred[0]))
        if np.amax(self.model.decision_function(X_pred)) < 0.03 :
            response = "I'm not sure I understood your question"
            # At this point of time, bot should save the question
            
        else:
            response = self.target_dictionary.get(y_pred[0])
        
        return response