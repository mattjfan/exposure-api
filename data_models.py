from neomodel import (BooleanProperty, DateTimeProperty, ArrayProperty,
StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, StructuredRel)

#Relationships Defined
#Relationship that defines when a person went to a building
class WentToPlaceRel(StructuredRel):
    enteredPlace = DateTimeProperty()
    #leftPlace = DateTimeProperty()

#Relationship that defines when two people contact eachother, and how
class ContactWithRel(StructuredRel):
    timeOfContact = DateTimeProperty(required=True)
    CONTACT_METHODS = {'L': 'Location', 'P': 'Personal Contact'}
    typeOfContact = StringProperty(choices=CONTACT_METHODS)

    #tim = Person(sex='M').save()
    #tim.sex # M
    #tim.get_sex_display() # 'Male'


#Model Schema Defined
class Person(StructuredNode):
    name = StringProperty()
    identifier = StringProperty(unique_index=True, required=True)
    phoneNumber = StringProperty()
    TESTING_STATUS_LIST = {'YES_WAITING': 'YES_WAITING', 'YES_NEGATIVE': 'YES_NEGATIVE', 'YES_POSITIVE':'YES_POSITIVE', 'NO_DENIED':'NO_DENIED', 'NO':'NO'}
    tested_status = StringProperty(choices=TESTING_STATUS_LIST)
    test_date = DateTimeProperty()
    symptoms_date = DateTimeProperty()
    additional_info = StringProperty()
    symptoms = ArrayProperty()
    atRisk = BooleanProperty()
    wentToPlaces = RelationshipTo('Place', 'VISITED', model=WentToPlaceRel)
    contactWithPeople = RelationshipTo('Person', 'CONTACTED', model=ContactWithRel)

class Place(StructuredNode):
    gpsLAT = StringProperty()
    gpsLon = StringProperty()
    identifier = StringProperty(unique_index=True, required=True)
    didInfectedPersonComeHere = BooleanProperty()    
    didSymptomaticPersonComeHere = BooleanProperty()

