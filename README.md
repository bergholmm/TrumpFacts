TrumpFacts
======
Visualise Trumps twitter feed in Kibana

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
- Run 'python3 main.py' to fetch and index tweets from twitter
- Run 'python3 main.py 'indexFromFile'' to read and index tweets from /Data


Thanks to
-----------

bpb27 for providing the full history of Trumps twitter wall:  
https://github.com/bpb27/trump_tweet_data_archive
