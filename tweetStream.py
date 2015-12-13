from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient

# Connect to your DB Server
client = MongoClient('YOUR_DATABASE_SERVER')
db = client.MiningTwitter
consumer_key = "YOUR_API_KEY"
consumer_secret = "YOUR_API_KEY"
access_token = "YOUR_API_KEY"
access_token_secret = "YOUR_API_KEY"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class MyStream(StreamListener):
        
    def on_status(self, status):
        print status.text
        
    def on_data(self, data):
        tweets = ""
        tweets += data.strip()         
        if (data.endswith("\r\n")):
            if tweets: 
                # Format tweet stream so it is acceptable by Mongo
                tweet = json.loads(tweets)
                # Insert into DB
                db.tweets.insert(tweet)
            tweets = ""
        return True
        
    def on_error(self, status):
        print status

twitterStream = Stream(auth, MyStream())
# Filter tweet stream to only include tweets in the Western New York area
twitterStream.filter(locations = [-78.9285,42.2362,-77.5992,43.1219])