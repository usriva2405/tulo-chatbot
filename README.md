# ml-bank-chatbot-telegram
ML based chatbot for banking applications

## Telegram Banking Bot
This bot is a generic conversational bot, designed for use case of a Banking App.
the packages are as below - 
1. nlp_query_parser - this contains implementation of vectorization algorithms. To implement a new vectorization algorithm, add as a class to vectorizers, and reference it in the vector_factory, followed by creating an enum in vector_types.
2. nlp_query_parser.model_selection - this contains classification models. Follows the same pattern as vectors above. I've not implemented all the algorithms.

N. B. - I'm still learning how to structure a python project. Please feel free to point out better implementations. 

While this is a prelim work, I intend to grow/ mature it and make it production ready. Please feel free to make contributions to it wherever necessary. (Raise a merge request)

Note on using Telegram : It is quite easy to prototype chatbots with Telegram-bot-api. however, the telegram class has been kept separate from the actual bot implementation.
So going forward, the same bot can be extended to facebook messenger, whatsapp business api, wechat and any other messaging app.

## Dataset
queries can be added to consumer_questions.csv
the dataset has been segregated into following query topic types - 
1. balance-inquiry
2. transaction-history-inquiry
3. card-block
4. card-unblock
5. introduction
6. small-talk
7. expletive
8. escalation

responses can be of 2 types - 
1. static-query
2. dynamic-query - can be used for creating JSON responses (if flask is used), with indication for placeholders. currently dummy values have been used.

# TODO
this is just a start. Following items are top of my mind, apart from few others - 
1. Improve classification
2. Create Flask APIs
3. Improve architecture
4. Add error handling
