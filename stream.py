from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient
client = MongoClient('mongodb://miningData:yaytwitter.jpg@192.241.162.199:27017/MiningTwitter')
db = client.MiningTwitter
consumer_key = "8L5XKUz1vUVy8d6QHWxRkij9t"
consumer_secret = "vc2zB116RFlk2v8lDlegkkaG7I4NNG168dTEq84W1XFCwjqrk3"
access_token = "38076141-9Ztkv2kSSkIn87lbl6OZDRfsyQ4dx6VCUoH5KeycP"
access_token_secret = "LkSqxdvXR8j17GpmiPPAyz57XvkPDdEzasi86g6GzTth6"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class MyStream(StreamListener):
    def __init__(self):
        self.user = []
        self.names = []
        self.text = []
        self.tweetCount = 0
        
    def on_status(self, status):
        print status.text
        
    def on_data(self, data):
        tweets = ""
        tweets += data.strip()         
        if (data.endswith("\r\n")):
            if tweets: 
                tweet = json.loads(tweets)
                db.tweets.insert(tweet)
                self.user.append(tweet['user']['screen_name'].encode('UTF-8'))
                self.names.append(tweet['user']['name'].encode('UTF-8'))
                self.text.append(tweet['text'].encode('UTF-8'))
                print "@" + self.user[self.tweetCount]
                print ''
                print self.names[self.tweetCount]
                print ''
                print self.text[self.tweetCount]
                print ''
                print '_____________________'
                print ''
                self.tweetCount += 1
                print self.tweetCount
                print ''
            tweets = ""
        return True
        
    def on_error(self, status):
        print status

twitterStream = Stream(auth, MyStream())
twitterStream.filter(locations = [-78.9285,42.2362,-77.5992,43.1219])