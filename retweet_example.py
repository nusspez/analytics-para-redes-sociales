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


for tweet in tweepy.Cursor(api.search, q='#ocean').items():
    try:
        # Add \n escape character to print() to organize tweets
        print('\nTweet by: @' + tweet.user.screen_name)
        print(tweet)
        print(dir(tweet))
        # Retweet tweets as they are found
        #tweet.retweet()
        print('Retweeted the tweet')
        print ("_____________________________________________________")

        sleep(5)

    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break