import flask
import neomodel
from flask import Flask, jsonify, request
from flask_api import status
from data_models import Person, Place, WentToPlaceRel, ContactWithRel
from neomodel import config


def create_new_user():
    content = request.get_json()
    try:
        phone_number = content['phoneNumber']
    except: 
        phone_number = None
    if (phone_number == None):
        return jsonify({'response': 'bad request, please try again and specify a \'phoneNumber\' parameter in the JSON request body'}, status.HTTP_400_BAD_REQUEST)
    else:
        try: 
            #iF THE PERSON IS Found properly, this applies
            existingPerson = Person.nodes.get(phoneNumber=phone_number)
        except (neomodel.exceptions.MultipleNodesReturned):
            return jsonify({'response': 'The Phoene Number' + phone_number + 'is already registered with multiple users'}, status.HTTP_403_FORBIDDEN)
        except (neomodel.exceptions.DoesNotExist): 
            #iF THE PERSON IS NOT FOUND, this applies
            newUser = Person(phoneNumber=phone_number).save()
            return jsonify({'response': 'new number created - ' + phone_number}, status.HTTP_200_OK)
        return jsonify({'response': 'The Phoene Number' + phone_number + 'is already a registered user'}, status.HTTP_403_FORBIDDEN)


def report_contact(personA, personB):
    return "contact!!!"

