import datetime
import uuid
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
    identifier = StringProperty(unique_index=True, required=True)
    phoneNumber = StringProperty()
    TESTING_STATUS_LIST = {'YES_WAITING': 'YES_WAITING', 'YES_NEGATIVE': 'YES_NEGATIVE', 'YES_POSITIVE':'YES_POSITIVE', 'NO_DENIED':'NO_DENIED', 'NO':'NO'}
    test_status = StringProperty(choices=TESTING_STATUS_LIST, default='NO')
    test_date = DateTimeProperty(default=lambda: datetime.datetime.now())
    symptoms_date = DateTimeProperty(default=lambda: datetime.datetime.now())
    additional_info = StringProperty(default="")
    symptoms = ArrayProperty(default=[])
    atRisk = BooleanProperty(default=False)
    wentToPlaces = RelationshipTo('Place', 'VISITED', model=WentToPlaceRel)
    contactWithPeople = RelationshipTo('Person', 'CONTACTED', model=ContactWithRel)
    didReport = BooleanProperty(default=False)

class Place(StructuredNode):
    gpsLAT_LONG = StringProperty()
    gpsLONG = StringProperty()
    gpsLAT = StringProperty()


#if you are a proto-user, then the identifier returns a cell phone instead of a push token
class ProtoUser(StructuredNode):
    phone = StringProperty(required=True)
    contactedIds = ArrayProperty(default=[])
    identifier = StringProperty(unique_index=True, default=lambda: uuid.uuid1())
    