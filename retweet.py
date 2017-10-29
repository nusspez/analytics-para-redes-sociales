import tweepy
import tokens,os,json
from time import sleep

consumer_key    = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token    = os.environ['ACCESS_TOKEN']
access_secret   = os.environ['ACCESS_TOKEN_SECRET']

# Access and authorize our Twitter credentials from credentials.py


class Advertiser:
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def retweet(self, id, forecast):
        try:
            if self.is_potential_client(forecast):
                self.api.retweet(id)
                return True
        except tweepy.TweepError as e:
            error_code = json.loads(e.response.text)['errors'][0]['code']
            if error_code == 327:
                return True
        return False
    def is_potential_client(self, forecast):
        if forecast['confidence'] <= 0.5 or forecast['top_class']=='neutro':
            return False
        return True

    def get_status(self, id):
        return self.api.get_status(id)

    def update(self, msg, id):
        return self.api.update_status(msg, id)