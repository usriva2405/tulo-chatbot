import json
import logging
import os
import re
import sys
from modules.utils.yaml_parser import Config

from telegram import (ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

sys.path.insert(0, os.path.abspath('..'))

# Custom Modules
from modules.services.chat_service import ChatService

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
bankchat_app = ChatService()

QUERY, CANCEL = range(2)


def initialize():
    chat_service = ChatService()


def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        'Hi {0}! I am your bank bot. '
        'Send /cancel to stop talking to me.\n\n'
        'How can I help you regarding your account?'
        '\nBalance? History? Card Block? Anything else?'.format(user.first_name))

    return QUERY


def closing_statement(text):
    closing_words = re.compile("thank|Thank|no|No|thats|Thats|Thanks")
    if closing_words.search(text):
        return True
    else:
        return False


def query(update, context):
    user = update.message.from_user
    text = update.message.text
    if closing_statement(text) == True:
        logger.info("closing_statement = true %s: %s", user.first_name, update.message.text)
        # answer, answer_cat, question_cat = bankchat_app.predict_answer(text)
        answer = bankchat_app.predict_response("en-US", text)
        update.message.reply_text(answer)
        return CANCEL
    else:
        # predict response
        answer = bankchat_app.predict_response("en-US", text)
        logger.info('************************')
        logger.info('Prediction given by model')
        logger.info('************************')
        logger.info("answer : {0}".format(answer))

        # response = answer + '\n\n Can I help you with anything else?'

        logger.info("Query %s: %s", user.first_name, update.message.text)

        update.message.reply_text(extract_response(answer))

        return QUERY


def extract_response(answer):
    print("extracting response... :")
    # get response element, remove the opening and closing [], and replace ' with ", so that it is convertible to json
    if answer is not None:
        try:
            response_str = str(answer.get("response"))[1:-1].replace("'", '"')
            response = json.loads(response_str).get("text")
        except Exception as e:
            logger.error(e)
            response = "I think your query broke me. Try after some time!!"
    return response


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Happy to help!!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    initialize();
    # Read telegram token from config
    telegram_token = Config.get_config_val(key="auth", key_1depth="telegram", key_2depth="token")
    # telegram_token = config['telegram-token']
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUERY: [MessageHandler(Filters.text, query)],
            CANCEL: [CommandHandler('cancel', cancel)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
