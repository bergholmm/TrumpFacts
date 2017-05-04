import sys
from fetchFromTwitter import fetchTweets
from readFromFile import readTweets
from elasticsearch import Elasticsearch

es = Elasticsearch()

def twitter():
    print('Fetching tweets...')
    fetchTweets(es)
    print('Done.')

def file():
    print('Reading tweets...')
    readTweets(es);
    print('Done.')

def main():
    if (len(sys.argv) > 1):
        if(sys.argv[1] == 'file'):
            file()
        else:
            twitter()
    else:
        twitter()

if __name__ == '__main__':
    main()
