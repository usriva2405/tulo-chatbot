# -*- coding: utf-8 -*-
import pickle
import os
from modules.nlp_engine.model_builder.trainer import Trainer
from modules.services.auth_service import AuthService


class ChatService:

    # initialize trainer module
    trainer = Trainer()

    def __init__(self):
        print(os.getcwd())
        # load the model from disk
        filename_response = 'modules/saved_models/CLASSIFIER_TFIDF_LOGISTIC_RESPONSE_01.sav'
        self.response_predictor = pickle.load(open(filename_response, 'rb'))

    '''
    use this function to expose prediction
    '''
    def predict_response(self, lang, query):
        print('query received by bankchat_app')
        return self.response_predictor.predict(lang, query)
