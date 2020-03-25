import datetime
from flask import request
from flask_api import status

from utilities import make_response, unobfuscate, check_for_values_in_request, try_for_datetime_from_string
from database_access_helpers import (report_contact_between_individuals, 
report_visited_place,
retrieve_or_create_person_from_identifier,
retrieve_or_create_place_from_lat_and_long,
update_person_statistics)


def reportSicknessSum(r): 

    #Step 1, Check to make sure all parameters are there
    content = request.get_json()
    necessary_values = ['identifier', 'tested_status', 'test_date', 'symptoms_date', 'symptoms', 'additional_info', 'contacted_individuals', 'visited_locations']
    isGoodRequest = check_for_values_in_request(necessary_values, content)
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter in the JSON request body.'}, status.HTTP_400_BAD_REQUEST)
    identifier = content['identifier']
    tested_status = content['tested_status']
    test_date = content['test_date']
    symptoms_date = content['symptoms_date']
    symptoms = content['symptoms']
    additional_info = content['additional_info']
    contacted_individuals = content['contacted_individuals']
    visited_locations = content['visited_locations']


    #Step 2, Check to make sure all parameters are properly formatted/Valid, and then report those parameters to the DB
    push_id = unobfuscate(identifier, r)
    if (push_id == None or identifier == None):
        return make_response({'response': '\'identifier\' is invalid. Not Part of our database'}, status.HTTP_400_BAD_REQUEST)

    sender = retrieve_or_create_person_from_identifier(identifier)
    update_person_statistics(sender, tested_status, test_date, symptoms_date, symptoms, additional_info)

    #Step 3, report contacts
    for individual in contacted_individuals:
        is_cell_phone = False
        #3.A See that necessary variables exist
        try: 
            contacted_identifier = individual["identifier"]
        except: 
            contacted_identifier = None
        try: 
            contact_time = individual['contact_time']
        except:
            contact_time = None

        #If contact time is not valid, change it to current time as approximation
        contact_time = try_for_datetime_from_string(contact_time)

        #If contacted_identifier is valid, and it is not a cell phone number (there is a registered account),
        #then get the push notification code. 
        if (contacted_identifier != None and is_cell_phone == False):
            push_notification_code = unobfuscate(contacted_identifier, r)
        else:
            push_notification_code = None
        #Now, do processing for this individual number based on what data is available
        if ((contacted_identifier == None or push_notification_code == None) and is_cell_phone == False):
            print("skipping this number")
        elif (is_cell_phone == True):
            print("do cell phone number processing")
        else:
            contacted_individual = retrieve_or_create_person_from_identifier(contacted_identifier)

            #report to the database that the two individuals contacted
            report_contact_between_individuals(sender, contacted_individual, contact_time)

            #now, send the push notification to the contacted_individual:
            message = "We have a problem to report with your coronavirus exposure."       
            try:
                send_push_message(push_notification_code, message)
            except:
                print("failed to send push notification for some reason")
    
    #Step 4, Report and Store Locations
    for location in visited_locations:
        #4.A See that necessary variables exist
        try: 
            latitude = location["latitude"]
        except: 
            latitude = None
        try: 
            longitude = location["longitude"]
        except: 
            longitude = None
        try: 
            contact_time = location['contact_time']
        except:
            contact_time = None

        #If contact time is not valid, change it to current time as approximation
        contact_time = try_for_datetime_from_string(contact_time)

        #If contacted_identifier is valid, and it is not a cell phone number (there is a registered account),
        #then get the push notification code. 
        #Now, do processing for this individual number based on what data is available
        if (latitude == None or longitude == None):
            print("skipping this location")
        else:
            contacted_location = retrieve_or_create_place_from_lat_and_long(latitude, longitude)
            #report to the database that the location was visited
            report_visited_place(sender, contacted_location, contact_time)

    return make_response({'response': 'We sent the Push Notifications!!!'}, status.HTTP_200_OK)
