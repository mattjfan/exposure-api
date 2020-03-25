import uuid
import redis
import datetime

from flask import request
from flask_api import status
from utilities import make_response, check_for_values_in_request, send_message
from database_access_helpers import (retrieve_or_create_protouser_from_number,
 does_proto_user_exist)

def invite_new_user(r):
    content = request.get_json()
    necessary_values = ['phone', 'contacted', 'inviter_identifier']
    isGoodRequest = check_for_values_in_request(necessary_values, content)
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter(s) in the JSON request body.'}, status.HTTP_400_BAD_REQUEST)
    
    phone = content['phone']
    contacted = content['contacted']
    inviter_identifier = content['inviter_identifier']

    invite_message = "You've been invited to download Exposeure, an app that helps you track your exposure to COVID-19! Find out more at getmyexposure.com"
    if (contacted == "False"):
        didSend = send_message(invite_message, phone)
        if didSend:
            return make_response({'response': 'sent messsage to' + str(phone) + 'successfully!'}, status.HTTP_200_OK)
        else: 
            return make_response({'response': 'did not send messsage to' + str(phone) + 'successfully.'}, status.HTTP_200_OK)
    else:
        proto_user = retrieve_or_create_protouser_from_number(phone)
        current_proto_user_contacts = proto_user.contactedIds
        current_proto_user_contacts.append(inviter_identifier)
        proto_user.contactedIds = current_proto_user_contacts
        proto_user.save()
        proto_user_id = proto_user.identifier
        #link this identifier in redis to the push notification feature. 
        r.set(str(proto_user_id), phone)

        didSend = send_message(invite_message, phone)
        if didSend:
            return make_response({'response': 'sent messsage to' + str(phone) + 'successfully!', 'new_identifier': proto_user_id}, status.HTTP_200_OK)
        else: 
            return make_response({'response': 'did not send messsage to' + str(phone) + 'successfully.', 'new_identifier': proto_user_id}, status.HTTP_200_OK)

def sign_up(r): 
    content = request.get_json()
    necessary_values = ['phone', 'push_token']
    isGoodRequest = check_for_values_in_request(necessary_values, content)
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter(s) in the JSON request body.'}, status.HTTP_400_BAD_REQUEST)
    
    phone = content['phone']
    push_token = content['push_token']

    #Check if user exists
    doesHaveProto = does_proto_user_exist(phone)
    #if it does, get data from user
    contacted_individuals = []
    if doesHaveProto:
        proto_user = retrieve_or_create_protouser_from_number(phone)
        identifier = proto_user.identifier
        contactedIds = proto_user.contactedIds
        for contacted in contactedIds:
            contactedJSON = {"identifier": contacted, "contact_time": datetime.datetime.now()}
            contacted_individuals.append(contactedJSON)
        proto_user.delete()
    else: 
        identifier = uuid.uuid1()
    
    #Step 3, store ID in our redis cluster 
    r.set(str(identifier), push_token)
    return make_response({ "identifier": identifier, "contacted_individuals": contacted_individuals}, status.HTTP_200_OK)