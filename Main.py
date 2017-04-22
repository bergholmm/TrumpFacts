import tweepy
import re
import time
from datetime import datetime
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch

keyFile = open('keys', 'r')
cachedStopWords = stopwords.words("english")
es = Elasticsearch()

consumer_key = keyFile.readline().rstrip()
consumer_secret =  keyFile.readline().rstrip()
access_token = keyFile.readline().rstrip()
access_token_secret = keyFile.readline().rstrip()

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def removeStopWords(text):
    return ' '.join([word for word in text.split() if word not in cachedStopWords])

def tokenize(text):
    return tokens_re.findall(text)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    print('Fetching tweets...')
    count = 0;

    for status in tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump').items():
        count = count + 1
        time_stamp = status._json['created_at']
        text = removeStopWords(status._json['text'].lower())
        text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
        text = "".join(c if c not in ('!','.',':',',','"','-','?','…',';','&','(',')','\'') else ' ' for c in text)
        tokens = (preprocess(text))
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_stamp,'%a %b %d %H:%M:%S +0000 %Y'))
        dt = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

        for token in tokens:
            es.index(
                    index='twitter_trump',
                    doc_type='tweet',
                    body={
                        'timestamp': dt,
                        'text': token,
                        }
            )

        if (count % 100) == 0:
            print('%d tweets fetched...' % (count))

    print('%d tweets fetched in total...' % (count))
    print('Done.')


if __name__ == '__main__':
    main()
