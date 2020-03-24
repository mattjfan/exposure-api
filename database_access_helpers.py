import neomodel
from data_models import Person, Place, WentToPlaceRel, ContactWithRel


#Reports to database contact between two individuals, or an individual and a place 
def report_contact_between_individuals(reporter, contacted, contact_date_time):
    rel = reporter.contactWithPeople.connect(contacted, {"timeOfContact": contact_date_time})
    rel.save()

def report_visited_place(reporter, place, visited_date_time):
    rel = reporter.wentToPlaces.connect(place, {"entered": visited_date_time})
    rel.save()

#retrieves individuals + places from database if they already exist, or creates them if they dont. 
def retrieve_or_create_person_from_identifier(identifier):
    try:
        print("we are trying to retrieve the following person")
        print(identifier)
        identified_person = Person.nodes.get(identifier=identifier)
    
    except (neomodel.exceptions.MultipleNodesReturned):
            print("Ok that didn't work, because MultipleNodesReturned")
            return None
    except (neomodel.exceptions.DoesNotExist): 
        identified_person = Person(identifier=identifier).save()
        print("Ok, so we returned a brand new person!!")
    return identified_person


def retrieve_or_create_place_from_identifier(identifier):
    try:
        identified_place = Place.nodes.get(identifier=identifier)
    except:
        #if the person is not in the database, we create a new representation for them
        identified_place = Place(identifier=identifier).save()
    return identified_place

