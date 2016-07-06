# The collection module of GeoTweet

Requirements:
python2.7*
tweepy3.5.0

Edit ```config.py``` and set your Twitter API credentials (before you have to register your app at https://apps.twitter.com), the perimeter which you want to listen to and, optionally, the keywords the collected tweets should contain.

The collection process should be run in the background.

Logging is performed in ```collection.log```.

For stopping the collection process, send the SIGTERM signal (```kill -15 PID```).
