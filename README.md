# Tulo-Chatbot
This bot is a ML (machine learning) based intent (category) specific conversational bot, with following features -
1. This is domain agnostic. Provide it with right training data and it should work just fine out of the box (However to demonstrate a use-case, training data is for banking domain).
2. It has been designed to classify incoming query into categories
3. In case a query is unclassifiable, it is stored for later training
4. It is REST API driven (via flask). However, it can also be extended to any currently available social messaging app such as slack bot, skype bot, whatsapp, wechat, telegram (telegram prototype implemented. See below for reference)
5. APIs require authentication and authorization.
6. Models can be trained and retrained on the fly
7. Everything (model creation, training, querying) is database driven (MongoDB and Redis server for caching).
8. Supports multilingual training
9. Supports trainable expletive query management
10. Out of box deployment ready on Heroku (More on this later)
11. Extend model selection and vector selection to custom implementation

In Pipeline (major upgrades)
1. Each user account can support bots in multiple projects, each in multiple languages.
2. Will Support (in the pipeline) follow up queries, custom variables in input and output.
3. Small talk support (was part of version 1, but upon re-designing, this feature broke). Move to Spacy for small talk
4. Improve classification accuracy by using normalizer (for spelling mistakes), NLTK for preprocessing, Lemmatization and stemming
5. Add GUI for improved user experience (will mostly be a separate project)

## Tech/ Infra Stack
Python 3.6+
MongoDB
Heroku (for deployment)
Redis (for decentralized caching)

## Actors and Systems

Users -> Brokers -> Language -> TrainedClassifier
1. User - person who creates the chatbot. This bot can be deployed as a *"Bot as a Service"*.
2. Brokers - projects under which chat bots are created. User can create multiple brokers (Bank Bot, HR Bot, Restaurant Bot)
3. Language - Under each broker, each chatbot can deal in multiple languages, with a classifier trained per language. Language is passed as a input parameter.
4. TrainedClassifier - trained model for a given language. Refer to REQUEST objects below on how to make multi-lingual queries


## Project Structure
```bash
modules
    |
    |__ controllers
    |__ data
    |    |__ dao
    |    |__ db_model
    |    |__ dto
    |__ nlp_engine
    |    |__ classifier_instance
    |    |__ model_builder
    |    |__ model_selection
    |    |__ vector_selection
    |__ saved_models *not used anymore*
    |__ services
    |__ utils
```

1. Controllers - These contain endpoints exposed for flask and telegram (going forward for any other end point as well)
2. data -> dao - contains daos for mongodb
        -> db_model - all the models which are required by the project reside here
        -> dto - response objects mostly
3. nlp_engine -> classifier_instance - trained instance of a model, which is pickled and stored in database after training
        -> model_builder - contains training classes
        -> model_selection - contains models used for classification. Extend your models here
        -> vector_selection - contains vector implementations for bag of words models.
4. services - intermediate layer between controllers and dao, plus any other addendum requirements
5. utils - misc methods

## Setup and installation -
1. Setup mongodb. the sample data is available in docs -> db folder. create a database called tulo_bot and dump everything there
2. ensure modules defined in requirements.txt exist (TODO : make installation of all requirements script based)
3. setup redis.
4. provide appropriate url and credentials for mongo and redis in config.yaml

## Run Flask API -
1. run flask_controller.py

## APIs

### AUTHENTICATION
REQUEST
URL : /authenticate
body :
```
{
	"email" : "utkarshsrivastava.aiml@gmail.com",
	"password" : "password1"
}
```
RESPONSE
returns list of brokers (id + default language) available and a auth token

### RETRAIN
REQUEST
URL : /retrain
body :
```
{
	"token": "<<use token generated from login here>>",
	"broker_id" : "5d9e1f9d6ecaa9720db58964",
 	"lang" : "en-US"
}
```

### QUERY
REQUEST
URL : /query
body :
```
{
	"token": "<<use token generated from login here>>",
	"broker_id" : "5d9e1f9d6ecaa9720db58964",
	"lang" : "en-US",
	"query" : "Can you show my balance?"
}
```

### LOGOUT
REQUEST
URL : /logout
body :
```
{
	"token": "<<use token generated from login here>>"
}
```


For more details refer to (https://github.com/usriva2405/tulo-chatbot/wiki)