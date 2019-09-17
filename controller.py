#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 23:02:04 2019

@author: usrivastava
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Flask"

@app.route('/healthcheck')
def health_check():
    return "ok"

@app.route('/query')
def query():
    return "response"


if __name__ == '__main__':
    app.run()