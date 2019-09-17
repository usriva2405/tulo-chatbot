#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 00:33:46 2019

@author: usrivastava
"""

class QueryResponse:
    def __init__(self, answer, answer_cat, question_cat):
        self.answer = answer
        self.answer_cat = answer_cat
        self.question_cat = question_cat
        
        
    def toJSON(self):
        return {"answer": self.answer, "answer_category": self.answer_cat, "question_category": self.question_cat}