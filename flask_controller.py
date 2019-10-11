#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:02:04 2019

@author: usrivastava
"""

from flask import Flask, request, json
from modules.services.chat_service import ChatService
from modules.services.auth_service import AuthService
from modules.services.training_service import TrainingService
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)
chatService = ChatService()
authService = AuthService()
trainService = TrainingService()


@app.route('/', methods=['GET'])
def get_root():
    return "<html><head><title>Welcome to Tulo!</title></head><body><h1>Welcome to Tulo!</h1><body></html>"


@app.route('/healthcheck', methods=['GET'])
def health_check():
    return "ok"


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    # fetch request objects
    inquiry = data['query']
    lang = data['lang']
    user_email = data['email']

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


@app.route('/retrain', methods=['POST'])
def retrain():
    data = request.get_json()
    # fetch request objects
    token = data['token']
    lang = data['lang']
    broker_id = data['broker_id']

    logger.info("***************retraining started*******************")
    logger.info("token : {0}".format(token))
    logger.info("lang : {0}".format(lang))
    logger.info("broker_id : {0}".format(broker_id))

    answer = trainService.retrain(token, broker_id, lang)

    return json.dumps(answer)


@app.route('/authenticate', methods=['POST'])
def authenticate():

    data = request.get_json()
    # fetch request objects
    email = data['email']
    password = data['password']

    response = authService.authenticate_user(email=email, password=password)
    logger.info("response : {0}".format(response))
    return response.toJSON()


@app.route('/logout', methods=['POST'])
def logout():

    data = request.get_json()
    # fetch request objects
    token = data['token']

    response = authService.logout_user(token=token)
    logger.info("response : {0}".format(response))
    return response.toJSON()


if __name__ == '__main__':
    app.run()
