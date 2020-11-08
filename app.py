from flask import Flask,request,jsonify
from twilio.twiml.voice_response import VoiceResponse,Gather
import speech_recognition as sr
import urllib.request
import random    
import firebase_admin
from firebase_admin import credentials,firestore
import math
from twilio.rest import Client
import json 
from geopy.geocoders import Nominatim
import requests

genderDict = {'1':"Male",'2':"Female"}
workDict = {'1':"Plumbing",'2':"Carpenter",'3':"Daily Wage Worker",'4':"House hold worker"}

url  = 'http://1195d2acad93.ngrok.io/'
f = open('credentials.json',) 
  
data = json.load(f) 

geolocator = Nominatim(user_agent="Headout-App")
account_sid = data['account_sid']
auth_token = data['auth_token']
client = Client(account_sid, auth_token)
r = sr.Recognizer()


cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
orderAudio = ""

en  = {
        'message1':'Welcome to the Workers Helpline.',
        'message2':'This helpline is your one stop solution to daily work.',
        'message3':'Press 1 for english, Press 2 for Hindi, Press 3 for Kannada',
        'message4':'Thank you for choosing the language',
        'message5':'What is your Age ?',
        'message6':'Press 1 if you are male and Press 2 if you are female',
        'message7':'Press 1 if you are a Plumber, Press 2 if you are a Carpenter, Press 3 if you are a Daily wage worker, Press 4 if you are a House Worker',
        'message8':'What is your expected per day salary ?',
        'message9':'Please tell your Name and City separated by from',
        'message10':"Thank you for providing the age",
        "message11":"Thank you for providing the gender",
        "message12":"Thank you for selecting the occupation",
        "message13":"Thank you for telling the expected salary",
        "message14":"Thank you for telling the name and the city",
        'message15':'We wil start recording after the beep',
        "message16":"You are now successfully registered. You will receive all the daily wage notification directly on your mobile phone. Goodbye"
    }   

hi = {
    "message1": "\u0935\u0930\u094d\u0915\u0930\u094d\u0938 \u0939\u0947\u0932\u094d\u092a\u0932\u093e\u0907\u0928 \u092e\u0947\u0902 \u0906\u092a\u0915\u093e \u0938\u094d\u0935\u093e\u0917\u0924 \u0939\u0948\u0964",
    "message2": "\u092f\u0939 \u0939\u0947\u0932\u094d\u092a\u0932\u093e\u0907\u0928 \u0906\u092a\u0915\u0947 \u0926\u0948\u0928\u093f\u0915 \u0915\u093e\u0930\u094d\u092f \u0915\u093e \u090f\u0915 \u0938\u094d\u091f\u0949\u092a \u0938\u092e\u093e\u0927\u093e\u0928 \u0939\u0948\u0964",
    "message3": "\u0905\u0902\u0917\u094d\u0930\u0947\u091c\u0940 \u0915\u0947 \u0932\u093f\u090f 1 \u0926\u092c\u093e\u090f\u0902, \u0939\u093f\u0902\u0926\u0940 \u0915\u0947 \u0932\u093f\u090f 2 \u0926\u092c\u093e\u090f\u0902, \u0915\u0928\u094d\u0928\u0921\u093c \u0915\u0947 \u0932\u093f\u090f 3 \u0926\u092c\u093e\u090f\u0902",
    "message4": "\u092d\u093e\u0937\u093e \u091a\u0941\u0928\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message5": "\u0924\u0941\u092e\u094d\u0939\u093e\u0930\u0940 \u0909\u092e\u094d\u0930 \u0915\u094d\u092f\u093e \u0939\u0948\u0902 ?",
    "message6": "\u092f\u0926\u093f \u0906\u092a \u092a\u0941\u0930\u0941\u0937 \u0939\u0948\u0902 \u0924\u094b 1 \u0926\u092c\u093e\u090f\u0902 \u0914\u0930 \u092f\u0926\u093f \u0906\u092a \u092e\u0939\u093f\u0932\u093e \u0939\u0948\u0902 \u0924\u094b 2 \u0926\u092c\u093e\u090f\u0902",
    "message7": "\u092f\u0926\u093f \u0906\u092a \u092c\u0922\u093c\u0908 \u0939\u0948\u0902 \u0924\u094b 1 \u0926\u092c\u093e\u090f\u0902, \u092f\u0926\u093f \u0906\u092a \u092c\u0922\u093c\u0908 \u0939\u0948\u0902 \u0924\u094b 2 \u0926\u092c\u093e\u090f\u0902, \u092f\u0926\u093f \u0906\u092a \u090f\u0915 \u0926\u093f\u0939\u093e\u0921\u093c\u0940 \u092e\u091c\u0926\u0942\u0930 \u0939\u0948\u0902 \u0924\u094b 3 \u0926\u092c\u093e\u090f\u0902, \u092f\u0926\u093f \u0906\u092a \u090f\u0915 \u0939\u093e\u0909\u0938 \u0935\u0930\u094d\u0915\u0930 \u0939\u0948\u0902 \u0924\u094b 4 \u0926\u092c\u093e\u090f\u0902",
    "message8": "\u0906\u092a\u0915\u0947 \u092a\u094d\u0930\u0924\u093f \u0926\u093f\u0928 \u0915\u0947 \u0935\u0947\u0924\u0928 \u0915\u0940 \u0909\u092e\u094d\u092e\u0940\u0926 \u0915\u094d\u092f\u093e \u0939\u0948?",
    "message9": "\u0915\u0943\u092a\u092f\u093e \u0905\u092a\u0928\u093e \u0928\u093e\u092e \u0914\u0930 \u0936\u0939\u0930 \u0907\u0938\u0938\u0947 \u0905\u0932\u0917 \u0915\u0930\u0915\u0947 \u092c\u0924\u093e\u090f\u0902",
    "message10": "\u0909\u092e\u094d\u0930 \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message11": "\u0932\u093f\u0902\u0917 \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message12": "\u0935\u094d\u092f\u0935\u0938\u093e\u092f \u0915\u093e \u091a\u092f\u0928 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message13": "\u0905\u092a\u0947\u0915\u094d\u0937\u093f\u0924 \u0935\u0947\u0924\u0928 \u092c\u0924\u093e\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message14": "\u0928\u093e\u092e \u0914\u0930 \u0936\u0939\u0930 \u092c\u0924\u093e\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0927\u0928\u094d\u092f\u0935\u093e\u0926",
    "message15": "\u0939\u092e \u092c\u0940\u092a \u0915\u0947 \u092c\u093e\u0926 \u0930\u093f\u0915\u0949\u0930\u094d\u0921\u093f\u0902\u0917 \u0936\u0941\u0930\u0942 \u0915\u0930 \u0926\u0947\u0902\u0917\u0947",
    "message16": "\u0905\u092c \u0906\u092a \u0938\u092b\u0932\u0924\u093e\u092a\u0942\u0930\u094d\u0935\u0915 \u092a\u0902\u091c\u0940\u0915\u0943\u0924 \u0939\u094b\u0964 \u0906\u092a \u0905\u092a\u0928\u0947 \u092e\u094b\u092c\u093e\u0907\u0932 \u092b\u094b\u0928 \u092a\u0930 \u0938\u0940\u0927\u0947 \u0938\u092d\u0940 \u0926\u0948\u0928\u093f\u0915 \u0935\u0947\u0924\u0928 \u0905\u0927\u093f\u0938\u0942\u091a\u0928\u093e \u092a\u094d\u0930\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902\u0917\u0947\u0964 \u0905\u0932\u0935\u093f\u0926\u093e"
}

ka = {
    "message1": "\u0cb5\u0cb0\u0ccd\u0c95\u0cb0\u0ccd\u0cb8\u0ccd \u0cb8\u0cb9\u0cbe\u0caf\u0cb5\u0cbe\u0ca3\u0cbf\u0c97\u0cc6 \u0cb8\u0cc1\u0cb8\u0ccd\u0cb5\u0cbe\u0c97\u0ca4.",
    "message2": "\u0c88 \u0cb8\u0cb9\u0cbe\u0caf\u0cb5\u0cbe\u0ca3\u0cbf \u0ca6\u0cc8\u0ca8\u0c82\u0ca6\u0cbf\u0ca8 \u0c95\u0cc6\u0cb2\u0cb8\u0c95\u0ccd\u0c95\u0cc6 \u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0c92\u0c82\u0ca6\u0cc1 \u0ca8\u0cbf\u0cb2\u0cc1\u0c97\u0ca1\u0cc6 \u0caa\u0cb0\u0cbf\u0cb9\u0cbe\u0cb0\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.",
    "message3": "\u0c87\u0c82\u0c97\u0ccd\u0cb2\u0cbf\u0cb7\u0ccd\u200c\u0c97\u0cc6 1, \u0cb9\u0cbf\u0c82\u0ca6\u0cbf\u0c97\u0cbe\u0c97\u0cbf 2 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf, \u0c95\u0ca8\u0ccd\u0ca8\u0ca1\u0c95\u0ccd\u0c95\u0cc6 3 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf\u0cb0\u0cbf",
    "message4": "\u0cad\u0cbe\u0cb7\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0c86\u0caf\u0ccd\u0c95\u0cc6 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message5": "\u0ca8\u0cbf\u0ca8\u0ccd\u0ca8 \u0cb5\u0caf\u0cb8\u0ccd\u0cb8\u0cc1 \u0c8e\u0cb7\u0ccd\u0c9f\u0cc1 ?",
    "message6": "\u0ca8\u0cc0\u0cb5\u0cc1 \u0caa\u0cc1\u0cb0\u0cc1\u0cb7\u0cb0\u0cbe\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0ca8\u0cc0\u0cb5\u0cc1 \u0cb8\u0ccd\u0ca4\u0ccd\u0cb0\u0cc0\u0caf\u0cbe\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 2 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf\u0cb0\u0cbf",
    "message7": "\u0ca8\u0cc0\u0cb5\u0cc1 \u0caa\u0ccd\u0cb2\u0c82\u0cac\u0cb0\u0ccd \u0c86\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 1 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf, \u0ca8\u0cc0\u0cb5\u0cc1 \u0c95\u0cbe\u0cb0\u0ccd\u0caa\u0cc6\u0c82\u0c9f\u0cb0\u0ccd \u0c86\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 2 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf\u0cb0\u0cbf, \u0ca8\u0cc0\u0cb5\u0cc1 \u0ca6\u0cc8\u0ca8\u0c82\u0ca6\u0cbf\u0ca8 \u0c95\u0cc2\u0cb2\u0cbf \u0c95\u0cc6\u0cb2\u0cb8\u0c97\u0cbe\u0cb0\u0cb0\u0cbe\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 3 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf, \u0ca8\u0cc0\u0cb5\u0cc1 \u0cae\u0ca8\u0cc6 \u0c95\u0cc6\u0cb2\u0cb8\u0c97\u0cbe\u0cb0\u0cb0\u0cbe\u0c97\u0cbf\u0ca6\u0ccd\u0ca6\u0cb0\u0cc6 4 \u0c92\u0ca4\u0ccd\u0ca4\u0cbf\u0cb0\u0cbf",
    "message8": "\u0ca6\u0cbf\u0ca8\u0c95\u0ccd\u0c95\u0cc6 \u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0ca8\u0cbf\u0cb0\u0cc0\u0c95\u0ccd\u0cb7\u0cc6 \u0c8e\u0cb7\u0ccd\u0c9f\u0cc1?",
    "message9": "\u0ca6\u0caf\u0cb5\u0cbf\u0c9f\u0ccd\u0c9f\u0cc1 \u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0cb9\u0cc6\u0cb8\u0cb0\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0ca8\u0c97\u0cb0\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cac\u0cc7\u0cb0\u0ccd\u0caa\u0ca1\u0cbf\u0cb8\u0cbf \u0c8e\u0c82\u0ca6\u0cc1 \u0cb9\u0cc7\u0cb3\u0cbf",
    "message10": "\u0cb5\u0caf\u0cb8\u0ccd\u0cb8\u0ca8\u0ccd\u0ca8\u0cc1 \u0c92\u0ca6\u0c97\u0cbf\u0cb8\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message11": "\u0cb2\u0cbf\u0c82\u0c97\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c92\u0ca6\u0c97\u0cbf\u0cb8\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message12": "\u0c89\u0ca6\u0ccd\u0caf\u0ccb\u0c97\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c86\u0caf\u0ccd\u0c95\u0cc6 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message13": "\u0ca8\u0cbf\u0cb0\u0cc0\u0c95\u0ccd\u0cb7\u0cbf\u0ca4 \u0cb8\u0c82\u0cac\u0cb3\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb9\u0cc7\u0cb3\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message14": "\u0cb9\u0cc6\u0cb8\u0cb0\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0ca8\u0c97\u0cb0\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb9\u0cc7\u0cb3\u0cbf\u0ca6\u0ccd\u0ca6\u0c95\u0ccd\u0c95\u0cbe\u0c97\u0cbf \u0ca7\u0ca8\u0ccd\u0caf\u0cb5\u0cbe\u0ca6\u0c97\u0cb3\u0cc1",
    "message15": "\u0cac\u0cc0\u0caa\u0ccd \u0ca8\u0c82\u0ca4\u0cb0 \u0ca8\u0cbe\u0cb5\u0cc1 \u0cb0\u0cc6\u0c95\u0cbe\u0cb0\u0ccd\u0ca1\u0cbf\u0c82\u0c97\u0ccd \u0caa\u0ccd\u0cb0\u0cbe\u0cb0\u0c82\u0cad\u0cbf\u0cb8\u0cc1\u0ca4\u0ccd\u0ca4\u0cc7\u0cb5\u0cc6",
    "message16": "\u0ca8\u0cc0\u0cb5\u0cc1 \u0c88\u0c97 \u0caf\u0cb6\u0cb8\u0ccd\u0cb5\u0cbf\u0caf\u0cbe\u0c97\u0cbf \u0ca8\u0ccb\u0c82\u0ca6\u0cbe\u0caf\u0cbf\u0cb8\u0cbf\u0c95\u0cca\u0c82\u0ca1\u0cbf\u0ca6\u0ccd\u0ca6\u0cc0\u0cb0\u0cbf. \u0ca8\u0cbf\u0cae\u0ccd\u0cae \u0cae\u0cca\u0cac\u0cc8\u0cb2\u0ccd \u0cab\u0ccb\u0ca8\u0ccd\u200c\u0ca8\u0cb2\u0ccd\u0cb2\u0cbf \u0ca8\u0cc0\u0cb5\u0cc1 \u0c8e\u0cb2\u0ccd\u0cb2\u0cbe \u0ca6\u0cc8\u0ca8\u0c82\u0ca6\u0cbf\u0ca8 \u0cb5\u0cc7\u0ca4\u0ca8 \u0c85\u0ca7\u0cbf\u0cb8\u0cc2\u0c9a\u0ca8\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0ca8\u0cc7\u0cb0\u0cb5\u0cbe\u0c97\u0cbf \u0cb8\u0ccd\u0cb5\u0cc0\u0c95\u0cb0\u0cbf\u0cb8\u0cc1\u0ca4\u0ccd\u0ca4\u0cc0\u0cb0\u0cbf. \u0cb5\u0cbf\u0ca6\u0cbe\u0caf"
}

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return "Hello world"

@app.route('/index',methods=['GET','POST'])
def index():
    response = VoiceResponse()
    response.say(en['message1'],voice='Polly.Aditi',language="hi-IN")
    response.say(en['message2'],voice='Polly.Aditi',language="hi-IN")
    response.say(en['message3'],voice='Polly.Aditi',language="hi-IN")
    gather = Gather(num_digits=1,action='/language')
    response.append(gather)
    return str(response)

@app.route('/language',methods=['GET','POST'])
def language():
    response = VoiceResponse()
    if 'Digits' in request.values:
        language = int(request.values['Digits'])
        if language == 1:
            response.say(en['message4'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message5'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=2,action='/age/'+str(language))
            response.append(gather)
            return str(response)
        elif language == 2:
            response.say(hi['message4'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message5'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=2,action='/age/'+str(language))
            response.append(gather)
            return str(response)
        elif language == 3:
            response.say(ka['message4'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message5'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=2,action='/age/'+str(language))
            response.append(gather)
            return str(response)
        else:
            response.redirect('/index')
            return str(response)
    else:
        return str(response)

@app.route('/age/<language>',methods=['GET','POST'])
def age(language):
    response = VoiceResponse()
    if 'Digits' in request.values:
        age = int(request.values['Digits'])
        if int(language) == 1:
            response.say(en['message10'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message6'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/gender/'+language+"/"+str(age))
            response.append(gather)
            return str(response)
        elif int(language) == 2:
            response.say(hi['message10'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message6'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/gender/'+language+"/"+str(age))
            response.append(gather)
            return str(response)
        elif int(language) == 3:
            response.say(ka['message10'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message6'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/gender/'+language+"/"+str(age))
            response.append(gather)
            return str(response)
        else:
            response.redirect('/index')
            return str(response)

    else:
        response.redirect('/index')
        return str(response)

@app.route('/gender/<language>/<age>',methods=['GET','POST'])
def gender(language,age):
    response = VoiceResponse()
    if 'Digits' in request.values:
        gender = request.values['Digits']
        if int(language) == 1:
            response.say(en['message11'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message7'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/work/'+language+"/"+str(age)+"/"+str(gender))
            response.append(gather)
            return str(response)
        elif int(language) == 2:
            response.say(hi['message11'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message7'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/work/'+language+"/"+str(age)+"/"+str(gender))
            response.append(gather)
            return str(response)
        elif int(language) == 3:
            response.say(ka['message11'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message7'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/work/'+language+"/"+str(age)+"/"+str(gender))
            response.append(gather)
            return str(response)
        else:
            response.redirect('/index')
            return str(response)

    else:
        response.redirect('/index')
        return str(response)

@app.route('/work/<language>/<age>/<gender>',methods=['GET','POST'])
def work(language,age,gender):
    response = VoiceResponse()
    if 'Digits' in request.values:
        work = request.values['Digits']
        if int(language) == 1:
            response.say(en['message12'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message8'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/salary/'+language+"/"+str(age)+"/"+str(gender)+"/"+work)
            response.append(gather)
            return str(response)
        elif int(language) == 2:
            response.say(hi['message12'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message8'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=4,action='/salary/'+language+"/"+str(age)+"/"+str(gender)+"/"+work)
            response.append(gather)
            return str(response)
        elif int(language) == 3:
            response.say(ka['message12'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message8'],voice='Polly.Aditi',language="hi-IN")
            gather = Gather(num_digits=1,action='/salary/'+language+"/"+str(age)+"/"+str(gender)+"/"+work)
            response.append(gather)
            return str(response)
        else:
            response.redirect('/index')
            return str(response)

    else:
        response.redirect('/index')
        return str(response)

@app.route('/salary/<language>/<age>/<gender>/<work>',methods=['GET','POST'])
def salary(language,age,gender,work):
    response = VoiceResponse()
    if 'Digits' in request.values:
        salary = request.values['Digits']
        if int(language) == 1:
            response.say(en['message13'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message9'],voice='Polly.Aditi',language="hi-IN")
            response.redirect('/answer/'+language+'/'+age+'/'+gender+'/'+work+'/'+salary)
            return str(response)
        elif int(language) == 2:
            response.say(hi['message13'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message9'],voice='Polly.Aditi',language="hi-IN")
            response.redirect('/answer/'+language+'/'+age+'/'+gender+'/'+work+'/'+salary)
            return str(response)
        elif int(language) == 3:
            response.say(ka['message13'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message9'],voice='Polly.Aditi',language="hi-IN")
            response.redirect('/answer/'+language+'/'+age+'/'+gender+'/'+work+'/'+salary)
            return str(response)
        else:
            response.redirect('/index')
            return str(response)

    else:
        response.redirect('/index')
        return str(response)

@app.route("/answer/<language>/<age>/<gender>/<work>/<salary>", methods=['GET', 'POST'])
def voice(language,age,gender,work,salary):
    response = VoiceResponse()
    args = request.args
    if 'RecordingUrl' in args:
        orderAudio = getAudio(args['RecordingUrl'])
        print(orderAudio,language,age,gender,work,salary)
        name = ""
        place = ""
        try:
            orderAudio = orderAudio.lower()
            name = orderAudio.split("from")[0]
            place = orderAudio.split("from")[1]
        except:
            pass
        labourId = generateLaborId()
        labourInfo = {
            "name": name,
            "place":place.lower().strip(),
            "age":int(age),
            "perDaySalary":int(salary),
            "gender":genderDict[gender],
            "work":workDict[work],
            "phone":request.values['From'],
            "workId":int(work)
        }
        print(labourInfo)
        db.collection('labourers').document(str(labourId)).set(labourInfo)
        if int(language) == 1:
            response.say(en['message14'],voice='Polly.Aditi',language="hi-IN")
            response.say(en['message16'],voice='Polly.Aditi',language="hi-IN")
            response.hangup()
        elif int(language) == 2:
            response.say(hi['message14'],voice='Polly.Aditi',language="hi-IN")
            response.say(hi['message16'],voice='Polly.Aditi',language="hi-IN")
            response.hangup()
        elif int(language) == 3:
            response.say(ka['message14'],voice='Polly.Aditi',language="hi-IN")
            response.say(ka['message16'],voice='Polly.Aditi',language="hi-IN")
            response.hangup()
        return str(response)
    else:
        action = url+'answer/'+language+'/'+age+'/'+gender+'/'+work+'/'+salary
        if int(language) == 1:
            response.say(en['message15'],voice='Polly.Aditi',language="hi-IN",)
            response.record(
                action= action,
                method='GET',
                finish_on_key='*',
                transcribe=True,
                play_beep=True
            )
        elif int(language) == 2:
            response.say(hi['message15'],voice='Polly.Aditi',language="hi-IN",)
            response.record(
                action= action,
                method='GET',
                finish_on_key='*',
                transcribe=True,
                play_beep=True
            )
        elif int(language) == 3:
            response.say(ka['message15'],voice='Polly.Aditi',language="hi-IN",)
            response.record(
                action= action,
                method='GET',
                finish_on_key='*',
                transcribe=True,
                play_beep=True
            )
        print(str(response))
        return str(response)


@app.route('/sendsms')
def sendSms():
    data = request.args
    body = data.get('body')
    number = data.get('number')
    number = '+'+number
    try:
        message = client.messages.create(
            body=body,
            from_='+12054489824',
            to=number
        )
        print("hello")
        return jsonify({"success":True,"messageId":message.sid})
    except Exception as e:
        return f"An Error Occured: {e}",400

def getAudio(url):
    fileNames = url.split("/")
    fileName = fileNames[-1]
    urllib.request.urlretrieve(url, '/home/learner/Desktop/Headout/Twilio-IVR/Recordings/'+fileName+'.wav')
    file_audio = sr.AudioFile('/home/learner/Desktop/Headout/Twilio-IVR/Recordings/'+fileName+'.wav')

    with file_audio as source:
        audio_text = r.record(source)

    print(type(audio_text))
    orderAudio = r.recognize_google(audio_text) 
    print(orderAudio)
    return orderAudio

def generateLaborId():

    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return int(random_str)

if __name__ == "__main__":
    app.run(debug=True,port=3000)