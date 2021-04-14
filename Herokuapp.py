from flask import Flask, request,  jsonify, abort, render_template
from flask_restful import reqparse
import os, json, datetime
from flask_sqlalchemy import SQLAlchemy
#import hmac
#from hashlib import sha1
#from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE1_URL','sqlite:///students.sqlite3') # Dataase URI, get in HEROKU

db = SQLAlchemy(app)

class storyInsights(db.Model):

    __tablename__="story_insights"
    id = db.Column(db.Integer, primary_key = True)
    plataforma = db.Column(db.String(30))
    idCliente = db.Column(db.String(30))
    timeStamp = db.Column(db.String(30))
    field = db.Column(db.String(10))
    idMedia = db.Column(db.String(30))
    impressoes = db.Column(db.String(10))
    alcance = db.Column(db.String(10))
    forward = db.Column(db.String(10))
    back = db.Column(db.String(10))
    exits = db.Column(db.String(10))
    replies = db.Column(db.String(10))
    
    def __init__(self, plataforma, idCliente, timeStamp, field, idMedia, impressoes, alcance, forward, back, exits, replies ): 
        self.plataforma = plataforma
        self.idCliente = idCliente
        self.timeStamp = timeStamp
        self.field = field
        self.idMedia = idMedia
        self.impressoes = impressoes
        self.alcance = alcance
        self.forward = forward
        self.back = back
        self.exits = exits
        self.replies = replies

@app.before_first_request
def create_tables():
    db.create_all()
# ------------------------LINES 9 /18 == ?

# ------------------------LINES 20 /21 == OK ?
testToken = 12345
token = os.environ.get('TOKEN', testToken)                          #DELETE ONCE DONE / We will use CONFIG VARS from Heroku once done      
#token = str(environ.get("TOKEN")) or 'token'        PUT BACK ONCE DONE/ CHEKC IF THIS WORKS IN HEROKU /make sure this is a striiiinngggg
received_updates = []

# ------------------------LINES 23 /26 == OK ?
@app.route('/', methods = ['GET'])
def home():
    #return str(received_updates) #STRINGIFY?
    #data = str(StoryInsights.query.all
    return (str(received_updates))

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

    return ('All Good')

@app.route('/instagram', methods = ['GET', 'POST'])
def getVerificationIG():
    parser = reqparse.RequestParser()
    parser.add_argument('hub.mode')
    parser.add_argument('hub.challenge')
    parser.add_argument('hub.verify_token') #, location='form' does not workcd ..
    parser.add_argument('object')
    parser.add_argument('envy')
    received_data = parser.parse_args()

    if request.method == 'GET':

        if received_data['hub.mode'] == 'subscribe' and received_data['hub.verify_token'] == token :
            return (str(received_data['hub.challenge']))

        return (str(received_data['hub.mode'])+' '+str(received_data['hub.verify_token'])+' '+str(received_data['hub.challenge']))

    if request.method == 'POST':
        data = request.get_json()

        responseJsonObject = data['object']
        responseJsonEntry = data['entry']
        for firstNestKey in responseJsonEntry:
            responseJsonId = firstNestKey['id']
            responseJsonTime = datetime.datetime.fromtimestamp(firstNestKey['time'])
            responseJsonChanges = firstNestKey['changes']
            for secondNestKey in responseJsonChanges:
                responseJsonField = secondNestKey['field']
                responseJsonValue = secondNestKey['value']
                responseJsonMediaId = secondNestKey['value']['media_id']
                responseJsonImpressions = secondNestKey['value']['impressions']
                responseJsonReach = secondNestKey['value']['reach']
                responseJsonForward = secondNestKey['value']['taps_forward']
                responseJsonBack = secondNestKey['value']['taps_back']
                responseJsonExits = secondNestKey['value']['exits']
                responseJsonReplies = secondNestKey['value']['replies']
                
        received_updates.append(data)

        sendtoDatabase = storyInsights(str(responseJsonObject), \
                                        str(responseJsonId), \
                                        str(responseJsonTime), \
                                        str(responseJsonField), \
                                        str(responseJsonMediaId), \
                                        str(responseJsonImpressions), \
                                        str(responseJsonReach), \
                                        str(responseJsonForward), \
                                        str(responseJsonBack), \
                                        str(responseJsonExits), \
                                        str(responseJsonReplies))
        db.session.add(sendtoDatabase)
        db.session.commit() 
    
        return ('200')


if __name__ == '__main__':
    app.run(debug=True, port=5000)