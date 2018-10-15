#!/usr/bin/env python

from __future__ import print_function
import sys
try:
   import rfc822
except ImportError as e:
   import rfc822py3 as rfc822
import time
import json
from sqlite3 import connect
try:
    from urllib import urlopen, urlencode
except ImportError as e:
    from urllib.request import urlopen
    from urllib.parse import urlencode
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
            print('No existing tweets found: requesting default timeline.',file=sys.stderr)
            tweet_count = load_tweets()
        else:
            print('Requesting tweets newer than %lu' % results[0],file=sys.stderr)
            tweet_count = load_tweets(since_id=results[0])
        if not tweet_count:
            going_up = False
    going_down = True
    while going_down:
        cu = c.cursor()
        cu.execute('SELECT MIN(tweet_id) min_id FROM `%s`' % Slug)
        results = cu.fetchone()
        print('Requesting tweets older than %lu' % results[0],file=sys.stderr)
        tweet_count = load_tweets(max_id=(results[0]-1))
        # The -1 is lame, but max_id is "<=" not just "<"
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    args = dict(count=20, slug=Slug,owner_screen_name=Screan_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/lists/statuses.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url)
    tweets=json.loads(user_timeline.decode('utf-8'))
    if type(tweets) == dict and u'errors' in tweets:
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
    print('''
Usage:

    %s <operation> <owner screen name> <slug name>

Operations:

    * init: Create an initial <owner screen name>_<slug name>.db file.
    * fetch: Fill in missing tweets for <owner screen name>_<slug name>.db

Example:
To get 'Top tech Jobs' list's tweet and store in 'ahmadfaizalbh_top-tech-jobs.db'
To create new DB file
%s init ahmadfaizalbh top-tech-jobs.db
and then
%s fetch ahmadfaizalbh top-tech-jobs.db
''' % (args[0],args[0],args[0]),file=sys.stderr)

def main(*args):
    global c, Screan_name, Slug
    if len(args) < 4:
        print_help(args)
    elif args[1] == 'init':
        Screan_name = args[2]
        Slug = args[3]
        try:
            c = connect('%s_%s.db' % (Screan_name,Slug))
            c.execute('CREATE TABLE `%s` (tweet_id INTEGER PRIMARY KEY NOT NULL,user TEXT NOT NULL,screan_name TEXT NOT NULL, description TEXT NOT NULL,\
created INTEGER NOT NULL, text TEXT NOT NULL, source TEXT)' % Slug)
        except Exception as e:
            print("Error: There was a problem creating your database: %s" % str(e),file=sys.stderr)
            sys.exit(-1)
    elif args[1] == 'fetch':
        Screan_name = args[2]
        Slug = args[3]
        try:
            c = connect('%s_%s.db' % (Screan_name,Slug))
        except Exception as e:
            print("Error: There was a problem opening your database: %s" % str(e),file=sys.stderr)
            sys.exit(-2)
        try:
            fetch()
        except Exception as e:
            print("Error: There was a problem retrieving %s's '%s' list: %s" % (Screan_name,Slug, str(e)),file=sys.stderr)
            print("Error: This may be a temporary failure, wait a bit and try again.",file=sys.stderr)
            sys.exit(-3)
    else:
        print_help(args)

if __name__ == '__main__':
    main(*sys.argv)
