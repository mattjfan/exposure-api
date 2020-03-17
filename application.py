import flask
from flask import Flask, jsonify
from flask_api import status

application = Flask(__name__)

@application.route('/')
def health_check():
    return jsonify({'response': 'health is ok'}, status.HTTP_200_OK)
