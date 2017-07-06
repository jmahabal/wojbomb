Wojbombs
========

This is a Twitter bot that re-tweets each original Woj tweet and classifies it according to how likely it thinks the news will shake-up the NBA.

Context
=======

Adrian Wojnarowski is a well-known NBA reporter. Over the past several years, he has broken several major stories about the NBA, mostly about where players were headed during Free Agency. NBA fans on the internet used the label `wojbombs` for these news tidbits, with `woj`+`nukes` or some other ballistic depending on the 'bigness' of the news. This bot attempts to do this classification automatically.

How it Works
============

The machine learning element is at the moment very, very naive. It takes in the past 3,000 or so tweets from Woj, filters it to only those that aren't re-tweets, and then runs a bi- and tri-gram CountVectorizer across the tweets. I then build a RandomForest Classifier model off of the tweets, with my target column the number of retweets the tweet received (biased against very recent tweets). 

I pickle this model, and then run each new tweet through it. To grab the tweets, I use Tweepy for access to the Twitter Stream, and filter it by original Woj tweets only.

I retweet the Woj tweet, along with the number of eventual retweets that the bot predicts it will have.

Most of the future work for this bot will be in the machine learning part. 