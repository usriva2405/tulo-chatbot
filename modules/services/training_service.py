import pickle
import os
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


class TrainingService:
    trainer = Trainer()

    @classmethod
    def retrain(cls, token, broker_id, lang):
        """
        this retrains the model and stores it in mongoDB
        :param token:
        :param broker_id:
        :param lang:
        :return:
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

                    trained_classifier = TrainedClassifierDao.get_trained_classifier(user=user, broker=broker, model_type=model_type, vector_type=vector_type, lang=lang)

                    if trained_classifier is not None:
                        trained_classifier_obj = cls.trainer.setup_model_weights(trained_classifier)

                        # save the pickled object to db
                        TrainedClassifierDao.save_classifier(user=user, broker=broker, model_type=model_type, vector_type=vector_type, lang=lang, classifier=trained_classifier_obj)
                        response = "Successfully re-trained"

                        # test if it was saved properly
                        cls.test_trainer(user=user, broker=broker, model_type=model_type, vector_type=vector_type, lang=lang)
                    else:
                        logger.info("could not find trained_classifier")
                        response = "could not find trained_classifier"
                else:
                    logger.info("Could not find broker")
                    response = "Could not find broker"

            else:
                logger.info("Unauthorized access/ session expired. Please re-login")
                response = "Unauthorized access/ session expired. Please re-login"
        except Exception as e:
            logger.error("error : {0}".format(e))
            response = "Error occurred"
        return response


    @classmethod
    def test_trainer(cls, user, broker, model_type, vector_type, lang):
        logger.info("inside test_trainer")
        classifier_instance = TrainedClassifierDao.get_trained_classifier_obj_from_db(user=user, broker=broker, model_type=model_type, vector_type=vector_type, lang=lang)
        logger.warning(classifier_instance)

        logger.info(classifier_instance.predict(user=user, broker=broker, model_type=model_type, vector_type=vector_type, lang=lang, query="hi"))
