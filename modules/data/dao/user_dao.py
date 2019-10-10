'''
Created on Thu Oct 10 13:51:19 2019

@author: usrivastava
@description:
    This is a dao for user
'''

import pandas as pd
import json
from modules.data.db_model.model import *
from modules.utils.yaml_parser import Config
from modules.utils.app_logger import AppLogger
from modules.utils.utility_functions import UtilityFunctions

logger = AppLogger()


class UserDao:

    @classmethod
    def get_user_by_email(cls, email):
        user = None
        if email is not None and email is not '':
            if UtilityFunctions.is_email_valid(email):
                user = User.objects(email__iexact=email)
            else:
                user = None
        else:
            user = None
        return user

    @classmethod
    def get_user_by_telegram_token(cls, telegram_token):
        user = None
        if telegram_token is not None and telegram_token is not '':
            user = User.objects(telegram_oAuth_token__iexact=telegram_token)
        else:
            user = None
        return user

    @classmethod
    def save_user(cls, first_name, last_name, email, password, age, gender, telegram_oAuth_token=None):
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, age=age, gender=gender,
                    telegram_oAuth_token=telegram_oAuth_token)
        user.save()
