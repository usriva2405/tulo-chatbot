#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 16:18:19 2019

@author: usrivastava
@description:

    RECOMMENDATION: change the filename when you change the model
"""

from modules.data.db_model.model import *
from modules.data.dto.base_response import BaseResponse
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class TrainedClassifierDao:

    @classmethod
    def save_classifier(cls, user, broker, model_type, vector_type, classifier, lang):
        """
        Use this function to save the file to database
        :param user:
        :param broker:
        :param model_type:
        :param vector_type:
        :param classifier:
        :param lang:
        :return:
        """
        response = None
        # training file location
        if user is not None:
            if broker is not None:
                if lang is not None:
                    if model_type is not None and vector_type is not None:
                        if classifier is not None:
                            trained_classifier = TrainedClassifier.objects(user=user, broker=broker, model_type=model_type,
                                                                   vector_type=vector_type, lang=lang)
                            if trained_classifier is None:

                                trained_classifier = TrainedClassifier(user=user, broker=broker, model_type=model_type,
                                                                       vector_type=vector_type, lang=lang,
                                                                       classifier=classifier)
                                trained_classifier.save()
                                response = BaseResponse(code=200, reason="successfully saved")
                            else:
                                # update the object instead of saving a new one
                                response = cls.update_classifier(user=user, broker=broker, model_type=model_type, vector_type=vector_type, classifier=classifier, lang=lang)
                        else:
                            response = BaseResponse(code=500, reason="classifier cannot be null")
                    else:
                        response = BaseResponse(code=500, reason="model type and vector type cannot be null")
                else:
                    response = BaseResponse(code=500, reason="lang cannot be null")
            else:
                response = BaseResponse(code=500, reason="broker cannot be null")
        else:
            response = BaseResponse(code=500, reason="user cannot be null")

        return response

    @classmethod
    def update_classifier(cls, user, broker, model_type, vector_type, classifier, lang):
        """
        Use this function to update the file to database
        :param user:
        :param broker:
        :param model_type:
        :param vector_type:
        :param classifier:
        :param lang:
        :return:
        """
        response = None
        # training file location
        if user is not None:
            if broker is not None:
                if lang is not None:
                    if model_type is not None and vector_type is not None:
                        if classifier is not None:
                            trained_classifier = TrainedClassifier.objects(user=user, broker=broker, model_type=model_type,
                                                                   vector_type=vector_type, lang=lang)
                            trained_classifier.update_one(set__classifier=classifier)
                            response = BaseResponse(code=200, reason="successfully updated")
                        else:
                            response = BaseResponse(code=500, reason="classifier cannot be null")
                    else:
                        response = BaseResponse(code=500, reason="model type and vector type cannot be null")
                else:
                    response = BaseResponse(code=500, reason="lang cannot be null")
            else:
                response = BaseResponse(code=500, reason="broker cannot be null")
        else:
            response = BaseResponse(code=500, reason="user cannot be null")

        return response

    @classmethod
    def get_classifier(cls, user, broker, model_type, vector_type, lang):
        """
        Use this function to save/ update the file to database
        :param user:
        :param broker:
        :param model_type:
        :param vector_type:
        :param classifier:
        :param lang:
        :return:
        """
        classifier = None
        # training file location
        if user is not None:
            if broker is not None:
                if lang is not None:
                    if model_type is not None and vector_type is not None:
                        classifier = TrainedClassifier.objects(user_id__all=[user], broker_id__all=[broker], model_type__all=[model_type],
                                                               vector_type__all=[vector_type], lang__all=[lang])
                    else:
                        logger.error("model type and vector type cannot be null")
                else:
                    logger.error("lang cannot be null")
            else:
                logger.error("broker cannot be null")
        else:
            logger.error("user cannot be null")

        return classifier
