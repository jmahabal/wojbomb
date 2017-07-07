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

def getWeapon(prediction):
    prediction = float(prediction)
    if prediction < 100:
        return "punch"
    elif prediction < 500:
        return "bullet"
    elif prediction < 2000:
        return "grenade"
    elif prediction < 5000:
        return "bomb 💣"
    else:
        return "nuke"

print "starting stream"

with open('secrets.json') as data_file:    
    secrets = json.load(data_file)

auth = tweepy.OAuthHandler(secrets["consumer_key"], secrets["consumer_secret"])
auth.set_access_token(secrets["access_key"], secrets["access_secret"])

api = tweepy.API(auth)

public_tweets = api.home_timeline()

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        status_id = status.id
        screenname = status.user.screen_name
        print status_id, screenname

        if screenname == "wojespn":
            print "from WOJ!"
            if not hasattr(status, 'retweeted_status'):
                prediction = predict(status.text)["prediction"]
                print status.text, prediction
                print status_id, screenname
                print "#woj" + getWeapon(prediction) + " (" + str(prediction) + ") " + " https://twitter.com/" + screenname + "/status/" + str(status_id)
                print "----------"

                # retweet with the tweet_id
                api.update_status("#woj"+ getWeapon(prediction) + " (" + str(int(prediction)) + " predicted retweets) " + " https://twitter.com/" + screenname + "/status/" + str(status_id))

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# wojespn: 50323173
# metaphoraminute: 575930104
# lelebronbot: 868212681014038528
myStream.filter(follow=['50323173'])
