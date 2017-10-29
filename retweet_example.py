import tweepy
import tokens,os,json
from time import sleep

consumer_key    = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token    = os.environ['ACCESS_TOKEN']
access_secret   = os.environ['ACCESS_TOKEN_SECRET']

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

api.retweet("924270051598979073")
print('Retweeted the tweet')
