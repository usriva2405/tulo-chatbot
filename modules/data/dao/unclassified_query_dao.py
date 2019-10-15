'''
Created on Sun Sep 22 22:26:19 2019

@author: usrivastava
@description:
    This is a dao for training data
'''

import pandas as pd
import json
from modules.data.db_model.model import *
from modules.data.dto.base_response import BaseResponse
from modules.utils.yaml_parser import Config
from datetime import datetime
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class UnclassifiedQueryDao:

    @classmethod
    def save_unclassified_query(cls, trained_classifier, query):
        """
        this method is used to save the queries which couldn't be classified correctly,
        or queries which could not qualify confidence threshold
        :param query: unclassified query
        :param trained_classifier: who created the broker. NOT THE PERSON WHO QUERIED
        :return:
        """
        response = None
        if trained_classifier is not None:
            if query is not None:
                unclassified_query = Unclassifiedquery(trained_classifier=trained_classifier, created_on=datetime.now(), query=query, is_trained=False, trained_on=None, train_category=None, is_discardable=True)
                unclassified_query.save()
                response = BaseResponse(code=200, reason="successfully saved")
            else:
                response = BaseResponse(code=500, reason="query cannot be empty. Could not save.")
        else:
            response = BaseResponse(code=500, reason="trained_classifier cannot be empty. Could not save")

        return response
