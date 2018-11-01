import csv
from datetime import timedelta

def download_csv(url):
    try:
        # Using Python2
        import urllib2
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
    except:
        # Using Python3
        import urllib.request
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
    raw_data = response.read().decode('ascii')
    return csv.reader(raw_data.split("\n")[1:])


def get_jams(today):
    data = download_csv("https://mathsjam.com/dates/")
    day1 = today.strftime("%Y-%m-%d")
    today += timedelta(days=1)
    day2 = today.strftime("%Y-%m-%d")
    out = []
    for row in data:
        if len(row) == 3:
            city,twitter,date = row
            if date in [day1,day2]:
                out.append(twitter)
    return out
