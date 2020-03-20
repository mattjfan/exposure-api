import flask
import neomodel
from flask import Flask, jsonify, request
from flask_api import status
import os
import json
import sys

from neomodel import config
from data_models import Person, Place, WentToPlaceRel, ContactWithRel
from create_user import create_new_user
from healthcheck import health_check
from push_notification import send_push_message


application = Flask(__name__)

config.DATABASE_URL = os.getenv('DATABASE_URL')

def log(x):
    print(x, file=sys.stdout)

def make_response(content, http_status = status.HTTP_200_OK ):
    # content = preserialize(content) # this was ported from cub's api for serializing custom objects jsonify doesn't recognize
    # Can add it here if we need it.
    return jsonify(content), http_status


@application.route('/')
def get_health():
    return health_check()

# TODO: Not Implemented.
# Should be a POST w/ data as an object w/ keys {
#   new_place_id,
#   old_place_id,
#   user_identifier
# }
# We should move the user_identifier from old_placed_id to new_place_id buckets
@application.route('/update-location', methods=["POST"])
def ingestLocationUpdate():
    data = json.loads(request.get_data())
    log(data)
    return make_response({}, status.HTTP_501_NOT_IMPLEMENTED)

# TODO: Not Implemented.
# Takes a place_id and returns the list of all user identifiers currently in that place_id bucket
# as an array with key 'tokens' (see skeleton code below)
@application.route('/get-contacted-ids', methods=["POST"])
def getContactedIds():
    data = json.loads(request.get_data())
    log(data)
    return make_response({ "tokens": []}, status.HTTP_501_NOT_IMPLEMENTED)

# TODO: Not Implemented
# Takes in an object with the push_token key set to the push notification key of the client
# Ingests the push token and associates it with a unique identifier alias
# returns an object with the unique identifier alias for that client.
@application.route('/request-identifier', methods=["POST"])
def ingestPushNotificationToken():
    data = json.loads(request.get_data())
    log(data)
    return make_response({ "identifier": ''}, status.HTTP_501_NOT_IMPLEMENTED)

#Create New User
#Takes a request with a JSON body with a phoneNumber parameter
@application.route('/create_new_user', methods=['POST'])
def createNewUser():
    return create_new_user()

#The application reports that a person has tested positive for coronavirus. From this application, they
#recieve a list of obfuscated ID's, the list of places a person has been to, and the diagnosis. 
#We use this data to notify the contacted individuals, and then record the necessary relations in our database.

#The List of sicknesses is reported as a JSON with the following structure: 


def unobfuscate(hidden_string):
    return hidden_string

#Here is an example of the API POST Request going to the server that comes from the phone
'''{
    "obfuscated_ID": "fdjhisjdfkjbsdkjfbsdk",
    "tested_positive": True, 
    "listed symptoms": ["wet_cough", "headache"],
    "symptom_description": "Lorem Ipsum but I might die!",
    "contacted_individuals": [
        {
            "obfuscated_ID": "kgkjsdbkjbfjhsdjfjsd"
            "contact_time": "25/01/2017 10:10:05"
        },
        {
            "obfuscated_ID": "kgkjsdbkjbfjhsdjfjsd"
            "contact_time": "25/01/2017 10:10:05"
        },
        {
            "obfuscated_ID": "kgkjsdbkjbfjhsdjfjsd"
            "contact_time": "25/01/2017 10:10:05"
        },
        {
            "obfuscated_ID": "kgkjsdbkjbfjhsdjfjsd"
            "contact_time": "25/01/2017 10:10:05"
        },
    ],
    "visited_places": [
        {
            "place_ID": "Bucket 1"
            "visit_time": "25/01/2017 10:10:05"
        },
        {
            "place_ID": "Bucket 1"
            "visit_time": "25/01/2017 10:10:05"
        },
    ],
    "phoneNumber": "301-536-2435"
}'''
@application.route('/report_sickness_or_positive_test', methods=['POST'])
def reportSickness(): 
    content = request.get_json()
    try:
        contacts = content['contacted_individuals']
    except: 
        contacts = None
    if (contacts == None):
        return jsonify({'response': 'bad request, there was no list of \'contacted_individuals\' from the request body (even an empty one)'}, status.HTTP_400_BAD_REQUEST)
    else:
        for individual in contacts:
            obfuscated_id = individual["obfuscated_id"]
            individual_id = unobfuscate(obfuscated_id)
            

            #now, send the push notification:
            message = "We have a problem to report with your coronavirus exposure."
            
            #WE NEED TO INCLUDE ERROR CHECKING HERE!!
            send_push_message(individual_id, message)

        return jsonify({'response': 'We sent the Push Notifications!!!'}, status.HTTP_200_OK)










#Record Place for User (person, GPS coordinates for place)
    #We get the place using our API (if used before we already have place saved so do not make google api call)

    #If in a new place, create a leave time for the previous place if it exists (if not, its ok), and set the start time for new place
    #If in the same place, do nothing 
    #Set Current Place in People to Place

#Record Contact Between Users (person, person)
    #If through Mesh Network, record Contact
    #If specified, record contact
    #Record time of Contact

#Get All Users in place at time (place, start time, end time)
    #Search through wentTo relations for a given place, amd then identify the people from there

#Mark Users At Risk

#Create New User

#Create New Place 


if __name__ == "__main__":
    application.run(debug=False)