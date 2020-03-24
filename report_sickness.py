import datetime
from flask import request
from flask_api import status

from utilities import make_response, unobfuscate
from database_access_helpers import (report_contact_between_individuals, 
report_visited_place,
retrieve_or_create_person_from_identifier,
retrieve_or_create_place_from_identifier)


def reportSicknessSum(r): 
    content = request.get_json()
    #Step 1, check for contacted individuals field
    try:
        contacts = content['contacted_individuals']
    except: 
        contacts = None
    #Step 2, check for identifier parameter
    try: 
        sender_id = content['identifier']
    except:
        sender_id = None

    if (contacts == None):
        return make_response({'response': 'bad request, there was no list of \'contacted_individuals\' from the request body (even an empty one)'}, status.HTTP_400_BAD_REQUEST)
    elif (sender_id == None):
        return make_response({'response': 'bad request, there was no \'identifier\' property in the request body'}, status.HTTP_400_BAD_REQUEST)

    else:
        true_sender_id = unobfuscate(sender_id, r)
        if (true_sender_id == None or sender_id == None):
            return make_response({'response': '\'sender_id\' is invalid. Not Part of our database'}, status.HTTP_400_BAD_REQUEST)

        sender = retrieve_or_create_person_from_identifier(sender_id)

        for individual in contacts:
            is_cell_phone = False
            #1 See that necessary variables exist
            try: 
                contacted_identifier = individual["identifier"]
            except: 
                contacted_identifier = None
            try: 
                contact_time = strptime(individual['contact_time'])
            except:
                contact_time = None


            #If contact time is not valid, change it to current time as approximation
            if (not isinstance(contact_time, datetime.datetime)):
                contact_time = datetime.datetime.now()

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

                #now, send the push notification to the :
                message = "We have a problem to report with your coronavirus exposure."       
                print("OK WE're Sending the push!!")     
                try:
                    send_push_message(push_notification_code, message)
                except:
                    #note that conversation failed
                    print("failed to send push notification for some reason")

        return make_response({'response': 'We sent the Push Notifications!!!'}, status.HTTP_200_OK)
