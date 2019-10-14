#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 00:33:46 2019

@author: usrivastava
"""
import logging
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class TelegramQueryResponse:

    @classmethod
    def extract_response(cls, answer):
        print("extracting response... :")

        # get response element, remove the opening and closing [], replace ' with ", so that it is convertible to json
        if answer is not None:
            try:
                response_str = str(answer.get("response"))[1:-1].replace("'", '"')
                response = json.loads(response_str).get("text")
            except Exception as e:
                logger.error(e)
                response = "I think your query broke me. Try after some time!!"
        return response
