# The collection module of GeoTweet

Requirements:
python2.7*
tweepy3.5.0

Edit ```config.py``` and set your Twitter API credentials (before you have to register your app at https://apps.twitter.com), the perimeter which you want to listen to and, optionally, the keywords the collected tweets should contain and the project name. The collected data will be recorded to a sqlite database with the name identical to the project name (+ ```.db``` extension).

The collection process should be run in the background.

Logging is performed in ```collection.log```. From the logs you can follow the number of collected tweets and potential exceptions and errors occurring while communicating with the Twitter API.

For stopping the collection process, send the SIGTERM signal (```kill -15 PID```).
