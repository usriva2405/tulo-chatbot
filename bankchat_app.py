# -*- coding: utf-8 -*-
import pickle

class BankApp:
    def __init__(self):
        # load the model from disk
        self.filename = 'saved_models/TFIDF_LOGISTIC_01_BANK_APP.sav'
        self.predictor = pickle.load(open(self.filename, 'rb'))

    '''
    use this function to expose prediction
    '''
    def predict_answer(self, query):        
        return self.predictor.predict(query)