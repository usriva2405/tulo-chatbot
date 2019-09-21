#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:02:04 2019

@author: usrivastava
"""

from flask import Flask, request, jsonify, json
import sys
import logging

from bankchat_app import BankApp
from modules.response_wrapper.query_response import QueryResponse


app = Flask(__name__)
bankchat_app = BankApp()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/healthcheck')
def health_check():
    return "ok"

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query = data['query']
    answer = bankchat_app.predict_answer(query)
    answer_category = bankchat_app.predict_answer_category(query)
    question_category = bankchat_app.predict_question_category(query)
    
    response = QueryResponse(answer, answer_category, question_category)
    logger.info('************************')
    logger.info('Prediction given by model')
    logger.info('************************')
    logger.info("answer : {0}".format(answer))
    logger.info("answer category : {0}".format(answer_category))
    logger.info("ques category : {0}".format(question_category))
    try:
        jsonStr = jsonify(response.toJSON())
    except:
        logger.info("error ", sys.exc_info()[0])
        jsonStr = None
        
    return jsonStr


if __name__ == '__main__':
    
    app.run()