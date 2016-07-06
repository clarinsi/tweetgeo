# The collection module of GeoTweet

Requirements:
python2.7*
tweepy3.5.0

Edit ```config.py``` and set your Twitter API credentials (before you have to register your app at https://apps.twitter.com) and the geographical perimeter which you want to listen to.

The collection process should be run in the background.

Logging is performed in ```collection.log```.

For stopping the collection process, send the SIGTERM signal (```kill -15 PID```).
