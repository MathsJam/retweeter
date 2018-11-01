from twitter import *
from get_jams import get_jams
from datetime import datetime
import config

twitter = Twitter(auth=OAuth(config.access_key, config.access_secret,
                             config.consumer_key, config.consumer_secret))

accounts = get_jams(datetime.now())

for jam in accounts:
    for tweet in twitter.statuses.user_timeline(screen_name=jam, count=10):
        if not tweet["retweeted"]:
            twitter.statuses.retweet(id=tweet["id"])
