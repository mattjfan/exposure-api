from flask import jsonify
from flask_api import status

def health_check():
    return jsonify({'response': 'health is ok'}, status.HTTP_200_OK)