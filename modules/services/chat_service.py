# -*- coding: utf-8 -*-
from modules.nlp_engine.model_builder.trainer import Trainer
from modules.services.auth_service import AuthService
from modules.data.dao.broker_dao import BrokerDao
from modules.data.dao.trained_classifier_dao import TrainedClassifierDao
from modules.utils.yaml_parser import Config
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class ChatService:
    '''
    use this function to expose prediction
    '''

    @classmethod
    def predict_response(cls, token, broker_id, lang, query):
        """
        This returns the prediction for a given query

        :param token: authentication session token
        :param broker_id: broker for which query is requested
        :param lang: language for which model was trained
        :param query: question being asked
        :return: response object
        """
        response = None
        logger.info("***************inside training service retrain*******************")
        try:

            # get user from token
            user = AuthService.get_logged_in_user(token=token)
            if user is not None:
                logger.info(user)
                broker = BrokerDao.get_broker_by_id(broker_id=broker_id)
                if broker is not None:
                    logger.info(broker)
                    model_type = Config.get_config_val(key="model", key_1depth="classifier", key_2depth="model")
                    vector_type = Config.get_config_val(key="model", key_1depth="vectorizer", key_2depth="vector")

                    logger.info(model_type)
                    logger.info(vector_type)

                    predictor = TrainedClassifierDao.get_trained_classifier_obj_from_db(user=user, broker=broker,
                                                                                        model_type=model_type,
                                                                                        vector_type=vector_type,
                                                                                        lang=lang)
                    if predictor is not None:
                        response = predictor.predict(lang, query)
                    else:
                        response = "could not find trained_classifier"
                else:
                    response = "Could not find broker"

            else:
                response = "Unauthorized access/ session expired. Please re-login"
        except Exception as e:
            logger.error("error : {0}".format(e))
            response = "Error occurred"

        logger.error(response)

        return response
