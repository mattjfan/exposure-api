from neomodel import (BooleanProperty, DateTimeProperty, 
StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, StructuredRel)

#Relationships Defined
#Relationship that defines when a person went to a building
class WentToPlaceRel(StructuredRel):
    enteredPlace = DateTimeProperty()
    leftPlace = DateTimeProperty()

#Relationship that defines when two people contact eachother, and how
class ContactWithRel(StructuredRel):
    timeOfContact = DateTimeProperty()
    CONTACT_METHODS = {'L': 'Location', 'P': 'Personal Contact'}
    typeOfContact = StringProperty(required=True, choices=CONTACT_METHODS)

    #tim = Person(sex='M').save()
    #tim.sex # M
    #tim.get_sex_display() # 'Male'


#Model Schema Defined
class Person(StructuredNode):
    name = StringProperty()
    phoneNumber = StringProperty(unique_index=True, required=True)
    didTestPositive = BooleanProperty()
    didHaveSymptomsButNoTest = BooleanProperty()
    timeOfPositiveTest = DateTimeProperty()
    #First Contact Information?
    atRisk = BooleanProperty()
    currentPlace = RelationshipTo('Place', 'CURRENT_PLACE')
    wentToPlaces = RelationshipTo('Place', 'VISITED', model=WentToPlaceRel)
    contactWithPeople = RelationshipTo('Person', 'CONTACTED', model=ContactWithRel)


class Place(StructuredNode):
    gpsCoordinates = StringProperty()
    isRecognizedByGoogleLocations = BooleanProperty()
    name = StringProperty()
    address = StringProperty()
    didInfectedPersonComeHere = BooleanProperty()
