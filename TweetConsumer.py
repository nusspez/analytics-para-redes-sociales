from kafka import KafkaConsumer
from ElasticSearchClient import ElasticSearchClient
from sendMongo import SendMongo
import collections,json
import numpy as np
import string


class TweetConsumer:
    def __init__(self,urlKafka,topic,urles,urlMongo):
        self.urlKafka = urlKafka
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic,bootstrap_servers=[self.urlKafka])
        self.urles = urles
        self.es = ElasticSearchClient(urles)
        self.urlMongo = urlMongo
        self.mongo = SendMongo(urlMongo)
    def receiveMessage(self):
        for message in self.consumer:
            tweet = json.loads(message.value.decode('utf8'))
            short_tweet = self.getRelevantFields(tweet)
            self.es.sendTweet('twitter','tweet',tweet['id'],short_tweet)
            #self.mongo.saveTweet("oswaldo",'tweet',iddoc,tweet)
            print(short_tweet)
    def getRelevantFields(self, tweet):
        copy = {
            "raw_text": tweet['text'],
            "text": cleanText(tweet["text"]),
            "created_at": tweet['created_at'],
            "user": {
                "id_str": tweet['user']['id_str'],
                "name": tweet['user']['name'],
                "id_str": tweet['user']['screen_name'],
            },
            "entities": {
                "hashtags": list(map(lambda h: h['text'], tweet['entities']['hashtags']))
            }
        }   
        return copy
def cleanText(text):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in text if ch not in exclude)

urles = "localhost:9200"
urlMongo = "54.174.5.92:27017"
urlKafka = "localhost:9092"
topic = "tweet"
consumer = TweetConsumer(urlKafka,topic,urles,urlMongo)
consumer.receiveMessage()