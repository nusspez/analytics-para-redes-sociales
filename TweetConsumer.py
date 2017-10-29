from kafka import KafkaConsumer
from ElasticSearchClient import ElasticSearchClient
from sendMongo import SendMongo
from forecasting import Watson
from retweet import Advertiser
import collections,json
import numpy as np
import string
import re


class TweetConsumer:
    def __init__(self,urlKafka,topic,urles,urlMongo,path_file):
        self.urlKafka = urlKafka
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic,bootstrap_servers=[self.urlKafka])
        self.urles = urles
        self.es = ElasticSearchClient(urles)
        self.urlMongo = urlMongo
        self.mongo = SendMongo(urlMongo)
        self.watson = Watson(path_file)
        self.ad = Advertiser()

    def receiveMessage(self):
        for message in self.consumer:
            tweet = json.loads(message.value.decode('utf8'))
            short_tweet = self.getRelevantFields(tweet)
            self.es.sendTweet('twitter','tweet',tweet['id'],short_tweet)
            #self.mongo.saveTweet("oswaldo",'tweet',iddoc,tweet)
            forecast = self.classify(short_tweet['text'],detail=True)
            output_str = "{}: {}\n{}: {}\n{}: {}\n{}: {}\n".format(
                forecast['top_class'],
                short_tweet['text'],
                forecast['classes'][0]['class_name'],
                forecast['classes'][0]['confidence'],
                forecast['classes'][1]['class_name'],
                forecast['classes'][1]['confidence'],
                forecast['classes'][2]['class_name'],
                forecast['classes'][2]['confidence'],
            )
            print(output_str)
            #self.ad.retweet(tweet['id'],forecast)
            if tweet['user']['name'] == 'mr octopus' or \
                    tweet['user']["screen_name"] == "MR_OOCTOPUS" or \
                    tweet['user']["id_str"] == "890452785002676225":
                pass
            else:
                if forecast['confidence'] <= 0.5 or forecast['top_class']=='neutro':
                    pass
                else:
                    if forecast['top_class'] == 'prestamo':
                        pub = '%s: Necesitas dinero BBVA esta contigo %s' % (tweet['user']['name'], tweet['text'])
                    elif forecast['top_class'] == 'inversion':
                        pub = '%s: No sabes como gastar tu dinero, en BBVA lo incrementas %s' % (tweet['user']['name'], tweet['text'])
                    self.ad.update(pub[:140], tweet['id'])



    def getRelevantFields(self, tweet):
        copy = {
            "raw_text": tweet['text'],
            "text": cleanText(tweet["text"]),
            "created_at": tweet['created_at'],
            "user": {
                "id_str": tweet['user']['id_str'],
                "name": tweet['user']['name'],
                "screen_name": tweet['user']['screen_name'],
            },
            "entities": {
                "hashtags": list(map(lambda h: h['text'], tweet['entities']['hashtags']))
            }
        }   
        return copy
    def classify(self, text, detail=False):
        return self.watson.classify(text, detail=detail)

def cleanText(text):
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    exclude = set(string.punctuation)
    return ''.join(ch for ch in text if ch not in exclude)

urles = "localhost:9200"
urlMongo = "54.174.5.92:27017"
urlKafka = "localhost:9092"
topic = "tweet"
path_file = '/home/kira/projects/analytics-para-redes-sociales/dataset.csv'

consumer = TweetConsumer(urlKafka,topic,urles,urlMongo, path_file)
consumer.receiveMessage()