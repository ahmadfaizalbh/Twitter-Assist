#!/usr/bin/env python
import sys
import rfc822
import time
import json
from sqlite3 import connect
from urllib import urlopen, urlencode
from tweetconnect import *
from auth_and_Secret import TweetOuth
c = None
Search_key = None
    
def fetch():
    going_up = True
    while going_up:
        cu = c.cursor()
        cu.execute('SELECT MAX(tweet_id) max_id FROM tweet')
        results = cu.fetchone()
        tweet_count = None
        if not results[0]:
            print >>sys.stderr, 'No existing tweets found: requesting default timeline.'
            tweet_count = load_tweets()
        else:
            print >>sys.stderr, 'Requesting tweets newer than %lu' % results[0]
            tweet_count = load_tweets(since_id=results[0])
        if not tweet_count:
            going_up = False
    going_down = True
    while going_down:
        cu = c.cursor()
        cu.execute('SELECT MIN(tweet_id) min_id FROM tweet')
        results = cu.fetchone()
        print >>sys.stderr, 'Requesting tweets older than %lu' % results[0]
        tweet_count = load_tweets(max_id=(results[0]-1))
        # The -1 is lame, but max_id is "<=" not just "<"
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    args = dict(count=20, q=Search_key)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/search/tweets.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    tweets=json.loads(user_timeline)
    if type(tweets) == dict and tweets.has_key(u'errors'):
        raise Exception(tweets[u'errors'])
    for twit in tweets[u'statuses']:
        c.execute('INSERT INTO tweet (user, tweet_id, created, text, source, screan_name, description) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (twit[u'user'][u'name'],
             twit['id'],
            time.mktime(rfc822.parsedate(twit['created_at'])),
            twit['text'],
            twit['source'],
            twit[u'user'][u'screen_name'],
            twit[u'user'][u'description']))
    c.commit()
    return len(tweets)

def print_help(args):
    print >>sys.stderr, '''
Usage:

    %s <operation> <search element>

Operations:

    * init: Create an initial <search element>.db file.
    * fetch: Fill in missing tweets for <search element>.db

example:
To search 'Cloud computing' and store in 'Cloud computing.db'
To create new DB file
%s init Cloud_computing
and then
%s fetch Cloud computing
''' % (args[0],args[0],args[0])

def main(*args):
    global c, Search_key
    if len(args) < 3:
        print_help(args)
    elif args[1] == 'init':
        Search_key = args[2]
        try:
            c = connect('%s.db' % Search_key)
            c.execute('CREATE TABLE tweet (tweet_id INTEGER PRIMARY KEY NOT NULL,user TEXT NOT NULL,screan_name TEXT NOT NULL, description TEXT NOT NULL, created INTEGER NOT NULL, text TEXT NOT NULL, source TEXT)')
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem creating your database: %s" % str(e)
            sys.exit(-1)
    elif args[1] == 'fetch':
        Search_key = args[2]
        for i in args[3:]:
            Search_key += ' ' + i
        try:
            c = connect('%s.db' % Search_key)
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem opening your database: %s" % str(e)
            sys.exit(-2)
        try:
            fetch()
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem retrieving %s's timeline: %s" % (Search_key, str(e))
            print >>sys.stderr, "Error: This may be a temporary failure, wait a bit and try again."
            sys.exit(-3)
    else:
        print_help(args)

if __name__ == '__main__':
    main(*sys.argv)
