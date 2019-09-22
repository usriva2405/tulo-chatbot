from mongoengine import *

connect("tulo_train")

class Circumstance(EmbeddedDocument):
    input_circumstance = StringField(required=False)
    output_circumstance = StringField(required=False)

class Variables(EmbeddedDocument):
    name = StringField(required=True) #number_1
    type = StringField(required=True) #@def.number
    value = StringField(required=True) #$number1
    io_type = StringField(required=True) #@def.input

class Response(EmbeddedDocument):
    text = ListField(StringField(required=False))
    custom = StringField(required=False)

#This is the final class
class Train(Document):
    lang = StringField(required=True)
    category = StringField(required=True)
    circumstance = EmbeddedDocumentField('Circumstance')
    variables = ListField(EmbeddedDocumentField('Variables'))
    training_queries = ListField(StringField(required=True))
    response = ListField(EmbeddedDocumentField('Response'))


