#busqueda en twitter
import tweepy, os
import tokens
import textwrap

CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN    = os.environ['ACCESS_TOKEN']
ACCESS_SECRET   = os.environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search,
                           q="quincena gastar",
                           count=20,
                           result_type="recent",
                           include_entities=True,
                           locations = [-118.65,14.39,-86.59,32.72],
                           lang="es").items():
                           a = tweet.text
                           #print(a)
                           print(textwrap.fill(a, 100))
                           print("")
