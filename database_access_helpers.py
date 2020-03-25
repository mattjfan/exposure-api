import neomodel
import datetime

from utilities import try_for_datetime_from_string
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
        identified_person = Person.nodes.get(identifier=identifier)
    
    except (neomodel.exceptions.MultipleNodesReturned):
            return None
    except (neomodel.exceptions.DoesNotExist): 
        identified_person = Person(identifier=identifier).save()
    return identified_person


#Takes in a person and parameters, and updates them appropriately. 
def update_person_statistics(individual,tested_status,test_date,symptoms_date, symptoms, additional_info):
    #Check to make sure tested status is valid enum, then update
    CANNON_TESTING_STATUS = ['YES_WAITING', 'YES_NEGATIVE', 'YES_POSITIVE', 'NO_DENIED', 'NO']
    if tested_status in CANNON_TESTING_STATUS:
        individual.tested_status = tested_status

    #Ensure that test_date is a valid date_time.
    individual.test_date = try_for_datetime_from_string(test_date)

    #Ensure that symptoms_date is a valid date_time.
    individual.symptoms_date = try_for_datetime_from_string(symptoms_date)

    #Add list of symptoms
    current_symptoms = individual.symptoms
    for item in symptoms:
        if (item not in current_symptoms):
            current_symptoms.append(item)
    individual.symptoms = current_symptoms

    #Set Additional Info Param
    individual.additional_info = additional_info

    individual.didReport = True
    
    individual.save()
    return individual


def retrieve_or_create_place_from_lat_and_long(latitude, longitude):
    lat_long = latitude + "+" + longitude
    try:
        identified_place = Place.nodes.get(gpsLAT_LONG = lat_long)
    except:
        #if the location is not in the database, we create a new representation for it
        identified_place = Place(gpsLAT_LONG = lat_long)
        identified_place.gpsLAT=latitude
        identified_place.gpsLONG=longitude
        identified_place.save()

    return identified_place

