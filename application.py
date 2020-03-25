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
from utilities import make_response, unobfuscate, check_for_values_in_request, send_message
from report_sickness import reportSicknessSum, get_reported_symptoms
from redis_place_interactions import ingest_location_update, get_contacted_ids
from invite_and_signup import invite_new_user, sign_up
from database_access_helpers import (report_contact_between_individuals, 
report_visited_place, retrieve_or_create_protouser_from_number,
retrieve_or_create_person_from_identifier, does_proto_user_exist)


application = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
#r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0, password=os.getenv('REDIS_PWD'))
#config.DATABASE_URL = os.getenv('NEO_DATABASE_URL')


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

@application.route('/report_sickness_or_positive_test', methods=['POST'])
def reportSickness():
    return reportSicknessSum(r) 

@application.route('/get_exposure_risk')
    #Confirmed Case Exposed - At Risk
    #Exposed to N people with Symptoms - Cautious
    #Not Exposed - Normal. 


@application.route('/invite-new-user', methods=['POST'])
def inviteNewUser():
    return invite_new_user(r)

@application.route('/signup', methods=['POST'])
def signUp(): 
    return sign_up(r)

@application.route('/get-symptoms')
def getReportedSymptoms():
    return get_reported_symptoms(r)


# Should be a POST w/ data as an object w/ keys {
#   new_place_id,
#   old_place_id,
#   identifier
# }
# We should move the identifier from old_placed_id to new_place_id buckets.
#If there is no old_place_id, please enter "None"
@application.route('/update-location', methods=["POST"])
def ingestLocationUpdate():
    return ingest_location_update(r)

# Takes a place_id and returns the list of all user identifiers currently in that place_id bucket
# as an array with key 'tokens' (see skeleton code below)
@application.route('/get-contacted-ids', methods=["POST"])
def getContactedIds():
    return get_contacted_ids(r)

if __name__ == "__main__":
    application.run(debug=False)