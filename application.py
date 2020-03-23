import flask
import neomodel
from flask import Flask, jsonify, request
from flask_api import status
import os
import json
import sys
import uuid
import redis
import datetime

from neomodel import config
from data_models import Person, Place, WentToPlaceRel, ContactWithRel
from create_user import create_new_user, ingestPushNotificationAndCreateID
from healthcheck import health_check
from push_notification import send_push_message
from utilities import make_response, unobfuscate
from report_sickness import reportSicknessSum
from database_access_helpers import (report_contact_between_individuals, 
report_visited_place,
retrieve_or_create_person_from_identifier,
retrieve_or_create_place_from_identifier)


application = Flask(__name__)
r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, password=os.getenv('REDIS_PWD'))
config.DATABASE_URL = os.getenv('NEO_DATABASE_URL')


@application.route('/')
def get_health():
    return health_check()


# Takes in an object with the push_token key set to the push notification key of the client
# Ingests the push token and associates it with a unique identifier alias
# returns an object with the unique identifier alias for that client.
@application.route('/request-identifier', methods=["POST"])
def ingestPushNotificationToken():
    return ingestPushNotificationAndCreateID(r)

#Create New User
#Takes a request with a JSON body with a phoneNumber parameter
@application.route('/create_new_user', methods=['POST'])
def createNewUser():
    return create_new_user()

#The application reports that a person has tested positive for coronavirus. From this application, they
#recieve a list of obfuscated ID's, the list of places a person has been to, and the diagnosis. 
#We use this data to notify the contacted individuals, and then record the necessary relations in our database.

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
    return reportSicknessSum(r) 


def send_text_message(phone_number):
    return True


# Should be a POST w/ data as an object w/ keys {
#   new_place_id,
#   old_place_id,
#   user_identifier
# }
# We should move the user_identifier from old_placed_id to new_place_id buckets.
#If there is no old_place_id, please enter "None"
@application.route('/update-location', methods=["POST"])
def ingestLocationUpdate():
    content = request.get_json()
    try:
        new_place_id = content['new_place_id']
    except: 
        return make_response({'response': 'bad request, please try again and specify a \'new_place_id\' parameter in the JSON request body'}, status.HTTP_400_BAD_REQUEST)
    try:
        old_place_id = content['old_place_id']
    except: 
        return make_response({'response': 'bad request, please try again and specify a \'old_place_id\' parameter in the JSON request body. If there is no old ID, set this parameter to \'None\''}, status.HTTP_400_BAD_REQUEST)
    try:
        user_identifier = content['user_identifier']
    except: 
        return make_response({'response': 'bad request, please try again and specify a \'user_identifier\' parameter in the JSON request body'}, status.HTTP_400_BAD_REQUEST)

    #remove from old bucket if there is one
    if(old_place_id != "None"):
        r.srem(old_place_id, user_identifier)
    
    #add to new bucket
    r.sadd(new_place_id, user_identifier)

    return make_response({'response': "Successfully added " + user_identifier + " to space " + new_place_id}, status.HTTP_200_OK)

# Takes a place_id and returns the list of all user identifiers currently in that place_id bucket
# as an array with key 'tokens' (see skeleton code below)
@application.route('/get-contacted-ids', methods=["POST"])
def getContactedIds():
    content = request.get_json()
    try:
        place_id = content['place_id']
    except: 
        return make_response({'response': 'bad request, please try again and specify a \'place_id\' parameter in the JSON request body'}, status.HTTP_400_BAD_REQUEST)
    try: 
        members = r.smembers(place_id)
    except:
        return make_response({"response":"That is an invalid place identifier"}, status.HTTP_404_NOT_FOUND)
    members = list(members)
    for i in range(len(members)): members[i]=str(members[i])

    return make_response({ "tokens": (members)}, status.HTTP_200_OK)




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