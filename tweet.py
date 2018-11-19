from __future__ import print_function
from twitter import *
from get_jams import get_jams
from datetime import datetime
import config
import sys

test = False
if "test" in sys.argv:
    test = True

twitter = Twitter(auth=OAuth(config.access_key, config.access_secret,
                             config.consumer_key, config.consumer_secret))

accounts = get_jams(datetime.now())
print(accounts)

def today(tweet):
    """Checks that the tweet is from today and not old"""
    now = datetime.now()
    if now.strftime("%Y") not in tweet["created_at"]:
        return False
    if now.strftime("%b %d") not in tweet["created_at"]:
        return False
    return True

for jam in accounts:
    try:
        tweets = twitter.statuses.user_timeline(screen_name=jam, count=10)
    except:
        if test:
            print("Error loading tweets from @"+jam)
        continue
    for tweet in tweets:
        if not tweet["retweeted"] and today(tweet):
            if test:
                print("If not testing, I would retweet this:","@"+jam,tweet["text"])
            else:
                twitter.statuses.retweet(id=tweet["id"])
