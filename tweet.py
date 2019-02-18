from __future__ import print_function
from twitter import Twitter,OAuth
from get_jams import get_jams
from datetime import datetime
from datetime import timedelta
import config
import sys
import logging

logger = logging.getLogger('tweet')

test = "test" in sys.argv

twitter = Twitter(auth=OAuth(config.access_key, config.access_secret,
                             config.consumer_key, config.consumer_secret))

all_jams = get_jams()
happening_jams = [jam for jam in all_jams if jam.happening()]

def today(tweet):
    """Checks that the tweet is from today and not old"""
    created_at = datetime.strptime(tweet["created_at"],"%a %b %d %H:%M:%S +0000 %Y")
    now = datetime.utcnow()
    return created_at > now - timedelta(days=1)

for jam in happening_jams:
    try:
        tweets = twitter.statuses.user_timeline(screen_name=jam.twitter, count=10)
    except:
        if test:
            logger.error("Error loading tweets from @"+jam)
        continue
    for tweet in tweets:
        if tweet["in_reply_to_status_id"] is None and not tweet["retweeted"] and today(tweet) and "retweeted_status" not in tweet:
            if test:
                logger.info("If not testing, I would retweet this:","@"+jam,tweet["text"])
            else:
                twitter.statuses.retweet(id=tweet["id"])
