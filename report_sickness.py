import datetime
from flask import request
from flask_api import status

from utilities import make_response, unobfuscate, check_for_values_in_request, try_for_datetime_from_string, send_message
from database_access_helpers import (report_contact_between_individuals, 
report_visited_place,
retrieve_or_create_person_from_identifier,
retrieve_or_create_place_from_lat_and_long,
update_person_statistics)


def isCellPhone(supposedNumber):
    #check if it is an int of 10 digits
    try:
        int(supposedNumber)
    except:
        return False
    if (len(supposedNumber) == 10):
        return True
    else:
        return False

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
        if (contacted_identifier != None):
            push_notification_code = unobfuscate(contacted_identifier, r)
        else:
            push_notification_code = None
        #Now, do processing for this individual number based on what data is available

        #Check if push notification code is actually a cell phone number
        if (push_notification_code != None):
            is_cell_phone = isCellPhone(push_notification_code)
        else:
            is_cell_phone = False

        if ((contacted_identifier == None or push_notification_code == None) and is_cell_phone == False):
            #Simply an invalid code
            print("skipping this number")
        elif (is_cell_phone == True):
            #DO THE PROCESSING FOR CELLULAR DEVICES
            print("do cell phone number processing")
            message = "A user of the Exposure App, who you have had contact with, has reported a change in their COVID-19 status. Download Exposure from getmyexposure.com to see your risk"
            phone_number = str(push_notification_code)[1:]
            successful_message = send_message(message, phone_number)
            if (successful_message == False):
                print("failed to send text message")
        else:
            #Do the process for push notifications
            contacted_individual = retrieve_or_create_person_from_identifier(contacted_identifier)
            #report to the database that the two individuals contacted
            report_contact_between_individuals(sender, contacted_individual, contact_time)
            #now, send the push notification to the contacted_individual:
            true_code = str(push_notification_code)[1:]
            print(true_code)
            message = "We have a problem to report with your coronavirus exposure."       
            try:
                send_push_message(true_code, message)
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

def get_reported_symptoms(r):
    content = request.get_json()
    necessary_values = ['identifier']
    isGoodRequest = check_for_values_in_request(necessary_values, content)
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter in the JSON request body.'}, status.HTTP_400_BAD_REQUEST)
    identifier = content['identifier']
    push_id = unobfuscate(identifier, r)

    if (push_id == None or identifier == None):
        return make_response({'response': '\'identifier\' is invalid. Not Part of our database'}, status.HTTP_400_BAD_REQUEST)
    else:
        individual = retrieve_or_create_person_from_identifier(identifier)
        response_json = {
            'tested_status': individual.tested_status,
            'symptoms': individual.symptoms,
            'additional_info': individual.additional_info,
            'test_date': individual.test_date,
            'symptoms_date': individual.symptoms_date,
            'has_response': individual.didReport
        }
        return make_response(response_json, status.HTTP_200_OK)