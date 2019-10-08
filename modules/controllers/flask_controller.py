#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:02:04 2019

@author: usrivastava
"""

from flask import Flask, request, json
from modules.services.chat_service import ChatService
from modules.utils.app_logger import AppLogger

app = Flask(__name__)
chatService = ChatService()

logger = AppLogger()


@app.route('/', methods=['GET'])
def get_root():
    return "<html><head><title>Welcome to Tulo!</title></head><body><h1>Welcome to Tulo!</h1><body></html>"


@app.route('/healthcheck', methods=['GET'])
def health_check():
    return "ok"


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    inquiry = data['query']
    lang = data['lang']
    answer = chatService.predict_response(lang, inquiry)

    logger.info('************************')
    logger.info('Prediction given by model')
    logger.info('************************')
    logger.info("answer : {0}".format(answer))
    logger.info('************************')

    # response = QueryResponse(answer)
    # print("****************************")
    # print("****************************")
    print(json.dumps(answer))
    # try:
    #     jsonStr = jsonify(response.toJSON())
    # except:
    #     logger.info("error ", sys.exc_info()[0])
    #     jsonStr = None

    return json.dumps(answer)


@app.route('/retrain', methods=['GET'])
def retrain():
    answer = chatService.retrain()

    return json.dumps(answer)


if __name__ == '__main__':
    app.run()
