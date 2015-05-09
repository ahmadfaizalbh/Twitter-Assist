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
Screan_name = None
Slug = None

    
def fetch():
    going_up = True
    while going_up:
        cu = c.cursor()
        cu.execute('SELECT MAX(tweet_id) max_id FROM `%s`' % Slug )
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
        cu.execute('SELECT MIN(tweet_id) min_id FROM `%s`' % Slug)
        results = cu.fetchone()
        print >>sys.stderr, 'Requesting tweets older than %lu' % results[0]
        tweet_count = load_tweets(max_id=(results[0]-1))
        # The -1 is lame, but max_id is "<=" not just "<"
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    args = dict(count=20, slug=Slug,owner_screen_name=Screan_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/lists/statuses.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    tweets=json.loads(user_timeline)
    if type(tweets) == dict and tweets.has_key(u'errors'):
        raise Exception(tweets[u'errors'])
    for twit in tweets:
        c.execute('INSERT INTO `%s` (user, tweet_id, created, text, source, screan_name, description) VALUES (?, ?, ?, ?, ?, ?, ?)' % Slug,
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

    %s <operation> <owner screen name> <slug name>

Operations:

    * init: Create an initial <owner screen name>.db file.
    * fetch: Fill in missing tweets for <owner screen name>.db

example:
To get 'text and data' list's tweet and store in 'dorait.db'
To create new DB file
%s init dorait text-and-data
and then
%s fetch dorait text-and-data
''' % (args[0],args[0],args[0])

def main(*args):
    global c, Screan_name, Slug
    if len(args) < 4:
        print_help(args)
    elif args[1] == 'init':
        Screan_name = args[2]
        Slug = args[3]
        try:
            c = connect('%s.db' % Screan_name)
            c.execute('CREATE TABLE `%s` (tweet_id INTEGER PRIMARY KEY NOT NULL,user TEXT NOT NULL,screan_name TEXT NOT NULL, description TEXT NOT NULL,\
created INTEGER NOT NULL, text TEXT NOT NULL, source TEXT)' % Slug)
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem creating your database: %s" % str(e)
            sys.exit(-1)
    elif args[1] == 'fetch':
        Screan_name = args[2]
        Slug = args[3]
        print Slug
        try:
            c = connect('%s.db' % Screan_name)
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem opening your database: %s" % str(e)
            sys.exit(-2)
        try:
            fetch()
        except Exception, e:
            print >>sys.stderr, "Error: There was a problem retrieving %s's '%s' list: %s" % (Screan_name,Slug, str(e))
            print >>sys.stderr, "Error: This may be a temporary failure, wait a bit and try again."
            sys.exit(-3)
    else:
        print_help(args)

if __name__ == '__main__':
    main(*sys.argv)
