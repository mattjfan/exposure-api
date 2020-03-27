from flask import request
from flask_api import status
from utilities import make_response, check_for_values_in_request
import os

#Removes all members from place_id, content being passed by Admin_Protected 
#Wrapper
def purge_place(r,content):

    necessary_values = ['place_id']

    isGoodRequest = check_for_values_in_request(necessary_values, content)
    
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter in the JSON request body.'}, status.HTTP_400_BAD_REQUEST)
    
    place_id = content['place_id']
    
    try: 
        members = r.smembers(place_id)
    except:
        return make_response({"response":"That is an invalid place identifier"}, status.HTTP_404_NOT_FOUND)
    
    members = list(members)

    for i in range(len(members)): members[i]=str(members[i])

    try: 
        r.srem(place_id,members)

        return make_response({"response":"place has been cleared"}, status.HTTP_200_OK)

    except: 
        return make_response({"response":"Something has gone wrong"}, status.HTTP_404_NOT_FOUND)

    
    



