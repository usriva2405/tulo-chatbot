# -*- coding: utf-8 -*-
import pickle
import os


class BankApp:
    def __init__(self):
        print(os.getcwd())
        # load the model from disk
        filename_response = 'modules/saved_models/CLASSIFIER_TFIDF_LOGISTIC_RESPONSE_01.sav'
        self.response_predictor = pickle.load(open(filename_response, 'rb'))

        # filename_ans_cat = 'modules/saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS_CATEGORY_02.sav'
        # filename_ques_cat = 'modules/saved_models/CLASSIFIER_TFIDF_LOGISTIC_QUESTIONS_CATEGORY_02.sav'
        # self.response_category_predictor = pickle.load(open(filename_ans_cat, 'rb'))
        # self.question_category_predictor = pickle.load(open(filename_ques_cat, 'rb'))

    '''
    use this function to expose prediction
    '''

    def predict_response(self, lang, query):
        print('query received by bankchat_app')
        return self.response_predictor.predict(lang, query)
