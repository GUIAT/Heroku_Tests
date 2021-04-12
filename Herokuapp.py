from flask import Flask, request,  jsonify, abort
from flask_restful import reqparse
import os
#import hmac
#from hashlib import sha1
#from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

# ------------------------LINES 9 /18 == ?

# ------------------------LINES 20 /21 == OK ?
testToken = 12345
token = os.environ.get('TOKEN', testToken)                          #DELETE ONCE DONE / We will use CONFIG VARS from Heroku once done      
#token = str(environ.get("TOKEN")) or 'token'        PUT BACK ONCE DONE/ CHEKC IF THIS WORKS IN HEROKU /make sure this is a striiiinngggg
received_updates = []

# ------------------------LINES 23 /26 == OK ?
@app.route('/', methods = ['GET'])
def home():
    return str(received_updates) #STRINGIFY?

# ------------------------LINES 28 /37 
@app.route('/facebook', methods = ['GET'])
def getVerificationFB():
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('entry')
    received_data = parser.parse_args()

    if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
        return (str(received_data['hub.challenge']))

    return (str(received_data['hub.mode'])+' '+str(received_data['hub.verify_token'])+' '+str(received_data['hub.challenge']))

@app.route('/instagram', methods = ['GET'])
def getVerificationIG():
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('entry')
    received_data = parser.parse_args()

    if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
        return int(received_data['hub.challenge'])

    return (str(received_data['hub.mode'])+' '+str(received_data['hub.verify_token'])+' '+str(received_data['hub.challenge']))


@app.route('/facebook', methods = ['POST'])
def getVerification():
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('entry')
    received_data = parser.parse_args()

    if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
        return int(received_data['hub.challenge'])

    return (str(received_data['hub.mode'])+' '+str(received_data['hub.verify_token'])+' '+str(received_data['hub.challenge']))


if __name__ == '__main__':
    app.run(debug=True, port=5000)