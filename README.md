## Tulo-Chatbot
This bot is a generic machine learning based conversational bot, designed for use case of a Banking App.
the packages are as below - 
1. nlp_query_parser - this contains implementation of vectorization algorithms. To implement a new vectorization algorithm, add as a class to vectorizers, and reference it in the vector_factory, followed by creating an enum in vector_types.
2. nlp_query_parser.model_selection - this contains classification models. Follows the same pattern as vectors above. I've not implemented all the algorithms.

N. B. - I'm still learning how to structure a python project. Please feel free to point out better implementations. 

While this is a prelim work, I intend to grow/ mature it and make it production ready. Please feel free to make contributions to it wherever necessary. (Raise a merge request)

For more details refer to (https://github.com/usriva2405/tulo-chatbot/wiki)

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
1. ~~Create Flask APIs - prediction function should be exposed via flask, so that it becomes implementation agnostic~~
2. Improve architecture
3. Add error handling and add comments
4. Add higher weightage to classes which fall in the category of expletives, or escalations - 
 - One way is to have separate models for various categories, for e.g., expletive, escalations and business specific queries.
 - Add a voting classifier on top of all models to correctly estimate the response
 
reason point 4 is required because the bot confuses between queries like "You're Cute" and "You're Stupid", and responds in a similar fashion.

5. Add normalizer to look for spelling mistakes
6. ~~Add lemmatization and stemming to improve accuracy~~
7. Add additional classifier for estimating category of question. This can be used to send input to selective classifier based on category.
8. Add follow-up queries support.
9. Add process to record unclassified queries
 - If system identifies an unclassified query, it should be appended, to be able to access at later stage, for retraining.
10. Restructure the training data storage. More on this below.
11. Move data to database instead of csv file. that ways, it would be better managed.
12. Implement an GUI for adding data/ training, once point 10 is completed.
13. Add Multi-lingual support.
