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

from modules.utils.app_logger import AppLogger

logger = AppLogger()


class ClassifierFile:

    @classmethod
    def save_classifier(cls, file):
        """
        Use this function to save/ update the file to database
        :param file: trained classifier to be saved
        :return: success/ failure
        """
        # training file location
        # save the model
