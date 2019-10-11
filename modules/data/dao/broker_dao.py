import pandas as pd
import json
from modules.data.db_model.model import *
from modules.data.dto.base_response import BaseResponse
from modules.data.dao.user_dao import UserDao
from modules.utils.yaml_parser import Config
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class BrokerDao:

    @classmethod
    def get_brokers_by_user_email(cls, email):
        brokers = []
        if email is not None:
            user = UserDao.get_user_by_email(email)
            logger.info("*******************************")
            logger.info(user)
            # use the user object to return broker list
            brokers = Broker.objects(user_id__all=[user])
            if len(brokers) > 0:
                brokers = list(brokers)
        else:
            logger.info("email cannot be null while fetching brokers list")

        return brokers

    @classmethod
    def get_broker_by_id(cls, broker_id):
        broker = None
        if broker_id is not None:
            broker = Broker.objects(pk=broker_id).first()
        else:
            logger.info("email cannot be null while fetching brokers list")

        return broker

    @classmethod
    def get_broker_ids_by_user_email(cls, email):
        broker_list = []
        if email is not None:
            brokers = cls.get_brokers_by_user_email(email)

            for broker in brokers:
                b = {
                    "id": str(broker.id),
                    "name": str(broker.broker_name),
                    "lang": str(broker.default_lang)
                }

                broker_list.append(b)
        else:
            logger.info("email cannot be null while fetching brokers list")

        return broker_list

    @classmethod
    def get_brokers_by_user_email_and_def_lang(cls, email, lang):
        brokers = []
        if email is not None and lang is not None:
            user = UserDao.get_user_by_email(email)

            # use the user object to return broker list
            brokers = Broker.objects(user_id__all=[user], default_lang__all=[lang])
            if len(brokers) > 0:
                brokers = list(brokers)
        else:
            logger.info("email cannot be null while fetching brokers list")

        return brokers

    @classmethod
    def create_broker_for_user(cls, email, broker_name, lang):
        response = None
        if email is not None and lang is not None:
            user = UserDao.get_user_by_email(email)

            # use the user object to return broker list
            broker = Broker(user_id=user, broker_name=broker_name, default_lang=lang)
            broker.save()
            response = BaseResponse(code=200, reason="broker created successfully")
        else:
            logger.info("email/ lang/ brokername cannot be null while saving broker")
            response = BaseResponse(code=500, reason="email/ lang/ brokername cannot be null while saving broker")
        return response
