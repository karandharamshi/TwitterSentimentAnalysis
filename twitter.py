import re
import tweepy
import numpy as np
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import json
import pymongo
from pymongo import MongoClient
try:
connect = MongoClient('localhost',27017)
print(connect)
print("Connected successfully!!!")
except:
print("Could not connect to MongoDB")
# you can use any database name in place of client_database2
db = connect['twitter']
print(db)
# you can use any collection name in place of client_collection1
collection = db.posts
print(collection)
class TwitterClient(object):
def __init__(self):
# get your keys and tokens from https://apps.twitter.com
consumer_key = 'yourkey'
consumer_secret = 'yoursecret'
access_token = 'yourtoken'
access_token_secret = 'yoursecrettoken'
# attempt authentication
try:
self.auth = OAuthHandler(consumer_key, consumer_secret)
self.auth.set_access_token(access_token, access_token_secret)
self.api = tweepy.API(self.auth)
except:
print("Error: Authentication Failed")
def clean_tweet(self, tweet):
return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
def get_tweet_sentiment(self, tweet):

analysis = TextBlob(self.clean_tweet(tweet))
if analysis.sentiment.polarity > 0:
return 'positive'
elif analysis.sentiment.polarity == 0:
return 'neutral'
else:
return 'negative'
def get_tweets(self, query, count = 1000):
tweets = []
try:
fetched_tweets = self.api.search(q = query, count = count)
for tweet in fetched_tweets:
parsed_tweet = {}
# saving text of tweet
parsed_tweet['text'] = tweet.text
# saving sentiment of tweet
parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
# appending parsed tweet to tweets list
if tweet.retweet_count > 0:
if parsed_tweet not in tweets:
tweets.append(parsed_tweet)
else:
tweets.append(parsed_tweet)
return tweets
except tweepy.TweepError as e:
print("Error : " + str(e))

api = TwitterClient()
tweet = {}
s=input("Enter query: ")
tweets = api.get_tweets(query = s, count = 1000)
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) -
len(ptweets))/len(tweets)))
print("\n\nPositive tweets:")
for tweet in ptweets[:10]:
print(tweet['text'])
print("\n\nNegative tweets:")
for tweet in ntweets[:10]:
print(tweet['text'])
labels = 'Positive', 'Negative', 'Neutral'
p=(100*len(ptweets)/len(tweets))
n=(100*len(ntweets)/len(tweets))
ne=(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))
sizes = [p, n, ne]
colors = ['yellowgreen', 'lightcoral', 'yellow']
explode = (0.1, 0, 0)
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.savefig('foo.png')
# Following code inserts the tweet and related sentiment of respective query into mongoDB
database
for t in tweets:
tweet = t
t1 = tweet['text']
s1 = tweet['sentiment']
post = {
"name" : s,
"text": t1,
"sentiment": s1
}
collection.insert(post)
while True:
print("\n1. Exit")
print("2. View data for particular query")

choice = int(input("Enter Choice: "))
if choice==1:
break
elif choice==2:
name = input("Enter Name: ")
posts1 = collection.find({'name':name})
c = 0
for post in posts1:
que=post
if c == 0:
print(que['name'])
c=c+1
print(que['text'])
print(que['sentiment'])