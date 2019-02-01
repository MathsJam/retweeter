import csv
from datetime import timedelta,datetime
from timezonefinder import TimezoneFinder
import pytz
import logging

logger = logging.getLogger('get_jams')

def download_csv(url):
    """Downloads and interprets a CSV"""
    try:
        # Using Python2
        import urllib2
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    except:
        # Using Python3
        import urllib.request
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            raw_data = response.read().decode('ascii')
        except urllib.error.HTTPError as e:
            logger.warning('Error fetching jam data: {}'.format(e))
            try:
                with open('dates.csv') as f:
                    raw_data = f.read()
            except FileNotFoundError:
                raise Exception("Couldn't load jam data")
    with open('dates.csv','w') as f:
        f.write(raw_data)
    return csv.DictReader(raw_data.split("\n"))

class Jam(object):
    def __init__(self, data):
        self.city = data.get('city')
        self.twitter = data.get('twitter')
        lat,lng = (data.get('latitude'),data.get('longitude'))
        try:
            lat,lng = float(lat), float(lng)
        except ValueError:
            raise Exception("Invalid latitude/longitude: '{}' and '{}'".format(lat,lng))
        if None not in (lat,lng):
            tf = TimezoneFinder()
            self.timezone = pytz.timezone(tf.timezone_at(lat=lat, lng=lng))
        else:
            self.timezone = None

        self.next_date = self.timezone.localize(datetime.strptime(data.get('next_date'),'%Y-%m-%d').replace(hour=19))

    def __str__(self):
        return '{city} (@{twitter}) next meeting {date} ({timezone})'.format(
                city=self.city,
                twitter=self.twitter,
                date=datetime.strftime(self.next_date,'%Y-%m-%d'),
                timezone=self.timezone
                )

    def happening(self, margin_hours=24):
        """ Is or was the Jam's start time within the given number of hours, relative to now? """
        now = pytz.utc.localize(datetime.utcnow())
        margin = timedelta(hours=margin_hours)
        begin = now - margin
        end = now + margin
        return begin < self.next_date < end


def get_jams():
    """Gets the Twitter handles of MathsJams that happen on the day given and the day after the day given"""
    data = download_csv("https://mathsjam.com/datesa/")
    jams = []
    for d in data:
        try:
            jam = Jam(d)
            jams.append(jam)
        except Exception:
            print("Invalid jam: {}".format(d))
    return jams
