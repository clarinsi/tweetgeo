# The collection module of TweetGeo

Requirements: python2.7* and tweepy3.5.0

Edit ```config.py``` and set your Twitter API credentials (before you have to register your app at https://apps.twitter.com), the perimeter which you want to listen to and the project name. The collected data will be recorded to a sqlite database with the name identical to the project name, ```[project_name].db```.

The collection process should be run in the background, like ```nohup python collection.py &```.

Logging is performed in ```[project_name].log```.  From the log you can follow the number of collected tweets and potential exceptions and errors occurring while communicating with the Twitter API.

For additional statistics regarding the collection process run ```stat.py```.

For stopping the collection process, send the SIGTERM signal (```kill -15 PID```).
