import tweepy
import time
from datetime import datetime
from tokenizeTweet import processText

keyFile = open('keys', 'r')
consumer_key = keyFile.readline().rstrip()
consumer_secret =  keyFile.readline().rstrip()
access_token = keyFile.readline().rstrip()
access_token_secret = keyFile.readline().rstrip()

def convertTime(time_stamp):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_stamp,'%a %b %d %H:%M:%S +0000 %Y'))
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

def index(tweets, es):
    count = 0
    for tweet in tweets:
        time_stamp = tweet._json['created_at']
        text = tweet._json['text'].lower()
        tokens = processText(text)
        dateTime = convertTime(time_stamp)

        for token in tokens:
            es.index(index='twitter_fetch_index', doc_type='tweet', body={ 'timestamp': dateTime, 'text': token, })

        count += 1
        if (count % 100) == 0:
            print('%d tweets indexed...' % (count))

    print('%d tweets fetched and indexed...' % (count))

def fetchTweets(es):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    index(tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump').items(), es)
