#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:02:04 2019

@author: usrivastava
"""

from flask import Flask, request, json
import logging

from modules.services.chat_service import ChatService

app = Flask(__name__)
bankchat_app = ChatService()

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
    inquiry = data['query']
    lang = data['lang']
    answer = bankchat_app.predict_response(lang, inquiry)

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


if __name__ == '__main__':
    app.run()
