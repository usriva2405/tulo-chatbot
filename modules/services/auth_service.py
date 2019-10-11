from cachetools import TTLCache
from modules.data.db_model.model import *
from modules.data.dto.base_response import BaseResponse
from modules.data.dto.auth_response import AuthResponse
from modules.data.dao.user_dao import UserDao
from modules.data.dao.broker_dao import BrokerDao
from modules.utils.utility_functions import UtilityFunctions
from modules.services.cache_service import CacheService


class AuthService:

    @classmethod
    def authenticate_user(cls, email, password):
        """
        this method is used for authenticating user
        :param email: user email
        :param password: TODO: hash it before storing in database/ checking against a value
        :return: returns auth token wrapped in object
        """
        response = None
        if email is not None and password is not None:
            if UserDao.is_user_authorized(email, password):

                # check if the email already exists in cache
                uuid = CacheService.get_object(email)

                if uuid is None:
                    # setup in cache

                    # generate a token and place it in cache against a uuid
                    uuid = UtilityFunctions.get_uuid()

                    # save email of user against the token in Time Sensitive cache if it does not exist already
                    # {key = token, value = email}
                    # token would be sent back in every session. use it to retrieve user before performing ops
                    CacheService.set_object(uuid, email)
                    # set a reverse lookup object as well
                    CacheService.set_object(email, uuid)

                else:
                    # refresh TTL for lookup and reverse-lookup for given user in Time Sensitive cache
                    # lookup pair : {key = token, value = email}
                    # reverse lookup pair : {key = email, value = token}
                    CacheService.set_object(uuid, email)
                    # set a reverse lookup object as well
                    CacheService.set_object(email, uuid)

                # retrieve list of brokers available to user
                broker_list = BrokerDao.get_broker_ids_by_user_email(email)
                response = AuthResponse(token=uuid, broker_list=broker_list)
            else:
                response = AuthResponse(token=None, broker_list=None, code=404, reason="email or password is incorrect")
        else:
            response = AuthResponse(token=None, broker_list=None, code=405, reason="email or password cannot be null")
        return response

    @classmethod
    def validate_auth_token(cls, token):
        response = None
        if token is not None:

            # get user email from cache using the token
            email = CacheService.get_object(token)

            if email is None:
                response = BaseResponse(code=404, reason="token is not valid. Please re-authenticate")
            else:
                # reset the counter of cache by re-storing the uuid and email in cache
                # this will extend the ttl for given token
                CacheService.set_object(token, email)
                CacheService.set_object(email, token)
                user = UserDao.get_user_by_email(email)
                response = BaseResponse(code=200, reason="successfully authenticated")
        else:
            response = BaseResponse(code=500, reason="token cannot be null")

        return response

    @classmethod
    def logout_user(cls, token):

        if token is not None:
            email = CacheService.get_object(token)
            if email is not None:
                CacheService.remove_objects(token)
                CacheService.remove_objects(email)
            else:
                CacheService.remove_objects(token)

        response = BaseResponse(code=200, reason="logged out successfully")
        return response

    @classmethod
    def get_logged_in_user(cls, token):
        """
        this method is used for getting logged in user
        :param token: session token
        :return: returns logged in user
        """
        user = None
        if token is not None:

            email = CacheService.get_object(token)

            if email is not None:
                user = UserDao.get_user_by_email(email)
            else:
                user = None
        else:
            user = None

        return user
