from flask import request
from flask_api import status
from utilities import make_response, check_for_values_in_request


def get_contacted_ids(r):
    content = request.get_json()
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

    return make_response({ "tokens": (members)}, status.HTTP_200_OK)


def ingest_location_update(r):
    content = request.get_json()
    necessary_values = ['new_place_id', 'old_place_id', 'identifier']
    isGoodRequest = check_for_values_in_request(necessary_values, content)
    if (isGoodRequest[0] == False):
        return make_response({'response': 'bad request, please try again and specify the ' + str(isGoodRequest[1]) + ' parameter(s) in the JSON request body. Note if there is no old_place_id, send "None" as the value'}, status.HTTP_400_BAD_REQUEST)
    
    new_place_id = content['new_place_id']
    old_place_id = content['old_place_id']
    user_identifier = content['identifier']

    #remove from old bucket if there is one
    if(old_place_id != "None"):
        r.srem(old_place_id, user_identifier)
    
    #add to new bucket
    r.sadd(new_place_id, user_identifier)

    return make_response({'response': "Successfully added " + user_identifier + " to space " + new_place_id}, status.HTTP_200_OK)