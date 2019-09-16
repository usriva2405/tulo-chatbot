# -*- coding: utf-8 -*-
import pickle

class BankApp:
    def __init__(self):
        # load the model from disk
        filename_ans = 'saved_models/CLASSIFIER_TFIDF_LOGISTIC_ANSWERS_01.sav'
        self.predictor = pickle.load(open(filename_ans, 'rb'))

    '''
    use this function to expose prediction
    '''
    def predict_answer(self, query):
        print('query received by bankchat_app')
        return self.predictor.predict(query)
    
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
        print(self.answer_predictor.predict("Hello"))