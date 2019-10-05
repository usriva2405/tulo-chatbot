#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 00:33:46 2019

@author: usrivastava
"""


class QueryResponse:
    def __init__(self, response):
        self.response = response.get("response")[0]
        print('*********QueryResponse************')
        print(self.response)
        self.input_circumstance = response.get("input_circumstance")[0]
        print(self.input_circumstance)
        self.output_circumstance = response.get("output_circumstance")[0]
        print(self.output_circumstance)
        self.variables = response.get("variables")[0]

    def toJSON(self):
        return {"response": self.response, "input_circumstance": self.input_circumstance,
                "output_circumstance": self.output_circumstance, "variables": self.variables}
