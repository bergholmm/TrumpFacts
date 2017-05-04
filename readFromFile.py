import glob
import os
import json
import time
from datetime import datetime
from tokenizeTweet import processText

path = './Data'

def convertTime(time_stamp):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_stamp,'%a %b %d %H:%M:%S +0000 %Y'))
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

def index(tweets, es):
    count = 0
    for tweet in tweets:
        time_stamp = tweet['created_at']
        text = tweet['text'].lower()
        tokens = processText(text)
        dateTime = convertTime(time_stamp)

        for token in tokens:
            es.index(index='twitter_file_index', doc_type='tweet', body={ 'timestamp': dateTime, 'text': token, })

        count += 1
        if (count % 100) == 0:
            print('%d tweets indexed...' % (count))

    print('%d tweets fetched and indexed...' % (count))

def readTweets(es):
    tweets = []
    for filename in glob.glob(os.path.join(path, '*.json')):
        print('Reading from %s...' % (filename))
        with open(filename) as data:
            d = json.load(data)
            tweets = tweets + d

    index(tweets, es)
