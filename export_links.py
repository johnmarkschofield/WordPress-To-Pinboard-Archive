#!/usr/bin/python

# Requires http://code.google.com/p/feedparser/
import feedparser
from bs4 import BeautifulSoup
import pinboard
import sys
import time

mailto_url = "mailto:"
base_url = "http://schof.org"
feed_url = "/feed/"
rate_limit_seconds = 4

def run_main(username, password):
    all_links = {}
    feedobj = feedparser.parse(base_url + feed_url)
    for item in feedobj['items']:
        all_links[item['links'][0]['href']] = item['title']
        item_text = item['content'][0]['value']
        soup = BeautifulSoup(item_text)
        for link in soup.findAll('a'):
            all_links[(link.get('href'))] = link.getText()



    pinboardobj = pinboard.open(username, password)
    for link in all_links.keys():
        time.sleep(rate_limit_seconds)
        print('Adding link %s (%s)' % (link, all_links[link]))
        if not link.startswith(mailto_url):
            pinboardobj.add(url = link,
                            description = all_links[link], 
                            extended = link,
                            tags = ("schof.org"))
    


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    run_main(username, password)
