import flask
import neomodel
from flask import Flask, jsonify
from neomodel import BooleanProperty, DateTimeProperty, StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, StructuredRel, config

from flask_api import status

application = Flask(__name__)

config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'

#Database Schema - Based
#Part 1, model to define the relationships between 

#Relationships Defined
#Relationship that defines when a person went to a building
class WentToPlaceRel(StructuredRel):
    enteredPlace = DateTimeProperty(
        default=lambda: datetime.now(pytz.utc)
    )
    leftPlace = DateTimeProperty()

#Relationship that defines when two people contact eachother, and how
class ContactWithRel(StructuredRel):
    timeOfContact = DateTimeProperty()
    isPersonalContact = BooleanProperty()
    isMeshContact = BooleanProperty()
    isSameLocationContact = BooleanProperty()


#______________________________________________________

#Model Schema Defined
class Person(StructuredNode):
    name = StringProperty()
    phoneNumber = StringProperty()
    didTestPositive = BooleanProperty()
    didHaveSymptomsButNoTest = BooleanProperty()
    timeOfPositiveTest = DateTimeProperty()
    wentToPlaces = RelationshipTo('Place', 'VISITED', model=WentToPlaceRel)
    contactWithPeople = RelationshipTo('Person', 'CONTACTED', model=ContactWithRel)


class Place(StructuredNode):
    gpsCoordinates = StringProperty()
    isRecognizedByGoogleLocations = BooleanProperty()
    name = StringProperty()
    address = StringProperty()
    didInfectedPersonComeHere = BooleanProperty()


class Book(StructuredNode):
    title = StringProperty(unique_index=True)
    author = RelationshipTo('Author', 'AUTHOR')

class Author(StructuredNode):
    name = StringProperty(unique_index=True)
    books = RelationshipFrom('Book', 'AUTHOR')


@application.route('/')
def health_check():
    return jsonify({'response': 'health is ok'}, status.HTTP_200_OK)

@application.route('/test2')
def testFlask2():
    harry_potter = Book(title='Harry potter and the..').save()
    rowling =  Author(name='J. K. Rowling').save()
    harry_potter.author.connect(rowling)
    return jsonify({'response': 'health is great!!!!!!!!!'}, status.HTTP_200_OK)





if __name__ == "__main__":
    application.run(debug=True)