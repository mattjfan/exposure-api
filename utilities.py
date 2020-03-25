import redis
import sys
import datetime

from flask import Flask, jsonify, request
from flask_api import status


def make_response(content, http_status = status.HTTP_200_OK ):
    # content = preserialize(content) # this was ported from cub's api for serializing custom objects jsonify doesn't recognize
    # Can add it here if we need it.
    return jsonify(content), http_status

def unobfuscate(hidden_string, r):
    return r.get(hidden_string)

def log(x):
    print(x, file=sys.stdout)

#if it is an id, it returns true. If it is an input number, it returns false
def isIDOrNumber(input_string):
    return False

#takes in a list of string values, and automates error checking to ensure that they're keys
#in the request. Returns [True, []] if they are all there, and [False, [list of missing values]]
#if there are missing values
def check_for_values_in_request(values_list, request_json):
    values_not_present = []
    all_values_present_in_request = True
    for value in values_list:
        try:
            value_present = request_json[value]
        except: 
            values_not_present.append(value)
            all_values_present_in_request = False
    return [all_values_present_in_request, values_not_present]


#returns a datetime opject. Currently, accepts "%d/%m/%Y %H:%M:%S" formatting! Can change as necessary.
def try_for_datetime_from_string(string_time):
    try: 
        my_time = datetime.datetime.strptime(string_time, "%d/%m/%Y %H:%M:%S")
    except:
        my_time = datetime.datetime.now()
    return my_time