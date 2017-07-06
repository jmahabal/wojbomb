from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

from sklearn.externals import joblib
import pandas as pd
import tweepy
import requests
import json

def predict(tweet_text):
	# Load our model and vectorizer
    clf = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    # Make the retweet count prediction after vectorizing the tweet 
    prediction = clf.predict(vectorizer.transform([tweet_text]).toarray())[0]

    # Return the prediction
    return {'prediction': prediction}

print "starting stream"

with open('secrets.json') as data_file:    
    secrets = json.load(data_file)
    for key in secrets:
        key = secrets[key]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # payload = {"tweet": status.text}
        prediction = predict(status.text)
        print status.text, prediction

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# wojespn: 50323173
myStream.filter(follow=['575930104']) # metaphor a minute
