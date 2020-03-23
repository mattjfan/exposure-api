import redis
import sys

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