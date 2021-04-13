from flask import Flask, request,  jsonify, abort, render_template
from flask_restful import reqparse
import os, json
from flask_sqlalchemy import SQLAlchemy
#import hmac
#from hashlib import sha1
#from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE1_URL','sqlite:///students.sqlite3') # Dataase URI, get in HEROKU

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class storyInsights(db.Model):
    id = db.Column('Index_Id', db.Integer, primary_key = True)
    responseJsonObject = db.Column(db.String(30))
    responseJsonEntry = db.Column(db.String(500))
    
    def __init__(self, responseJsonObject, responseJsonEntry):
        self.responseJsonObject = responseJsonObject
        self.responseJsonEntry = responseJsonEntry
    

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
    #return (render_template('show_all.html', storyInsights = storyInsights.query.all()))

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
        #data = request.json
        data = request.data
        #responseJsonObject = data['object']
        #responseJsonEntry = data['entry'] #SQL doesnt't accept dict -MUST CONVERT (with everything after the dot bug on sqlalchemy side /with error 500)
        
        #print(responseJsonEntry)
        #senddtoDatabase = storyInsights(theObject, theEntry)
        received_updates.append(data) 
        
        #db.session.add(theObject)
        #db.session.commit() 
    
        return ('200')
'''
@app.route('/instagram', methods = ['POST'])
def pushData():
    data = request.data
    theObject = received_data['object']
    theEntry = received_data['entry']
    received_updates.append(data)

    db.session.add(theObject, theEntry)
    db.session.commit() 
    
    return ('All Good')
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)