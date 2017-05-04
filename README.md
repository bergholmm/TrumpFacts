TrumpFacts
======
Python script to fetch trumps twitter feed and index the words of the tweets in elasticsearch.


Requirements
------------

- Elasticsearch 5.3.0
- Kibana 5.3.0 (To visualize the tweets)
- Twitter auth keys

Python requirements
------------

- Tweepy
- Elasticsearch
- nltk corpus

How to use
------------

- Start Elasticsearch and Kibana
- run python3 main.py to fetch and index tweets from twitter
- run python3 main.py 'file' to read and index tweets from /Data


Thanks to
-----------

bpb27 for providing the full history of Trumps twitter wall
Git repo: https://github.com/bpb27/trump_tweet_data_archive
