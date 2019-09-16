# -*- coding: utf-8 -*-
import pickle

class BankApp:
    def __init__(self):
        # load the model from disk
        filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS.sav'
        self.response_predictor = pickle.load(open(filename, 'rb'))
        filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS_CATEGORY.sav'        
        self.response_category_predictor = pickle.load(open(filename, 'rb'))
        filename = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_QUESTIONS_CATEGORY.sav'
        self.question_category_predictor = pickle.load(open(filename, 'rb'))

    '''
    use this function to expose prediction
    '''
    def predict_answer(self, query):
        print('query received by bankchat_app')
        return self.response_predictor.predict(query)
    
    '''
    use this function to expose prediction
    '''
    def predict_answer_category(self, query):        
        return self.response_category_predictor.predict(query)
    
    '''
    use this function to expose prediction
    '''
    def predict_question_category(self, query):        
        return self.question_category_predictor.predict(query)
    
    
    def test_prediction(self):
        print(self.response_predictor.predict("Hello"))