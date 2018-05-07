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
screen_name = None
repeat = False


class InvalidTokenError(ValueError):
    __module__ = None
    def __init__(self,*args,**kwargs):
        ValueError.__init__(self,*args,**kwargs)


def fetch():
    going_up = True
    while going_up:
        cu = c.cursor()
        cu.execute('SELECT MAX(tweet_id) max_id FROM tweet')
        results = cu.fetchone()
        tweet_count = None
        if not results[0]:
            print('No existing tweets found: requesting default timeline.',file=sys.stderr)
            tweet_count = load_tweets()
        else:
            print( 'Requesting tweets newer than %lu' % results[0])
            tweet_count = load_tweets(since_id=results[0])
        if not tweet_count:
            going_up = False
    going_down = True
    while going_down:
        cu = c.cursor()
        cu.execute('SELECT MIN(tweet_id) min_id FROM tweet')
        results = cu.fetchone()
        print ( 'Requesting tweets older than %lu' % results[0],file=sys.stderr)
        tweet_count = load_tweets(max_id=(results[0]-1))
        # The -1 is lame, but max_id is "<=" not just "<"
        if not tweet_count:
            going_down = False

def load_tweets(**kwargs):
    args = dict(count=20, trim_user=1, screen_name=screen_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    tweets=json.loads(user_timeline)
    print(tweets)
    if type(tweets) == dict and tweets.has_key(u'errors'):
        if repeat and tweets[u'errors'][0]["code"]==88:
            print (tweets[u'errors'][0]["message"],file=sys.stderr)
            time.sleep(1000) 
            return load_tweets(**kwargs)
        if tweets[u'errors'][0]["code"] in (32,89,99):
            raise InvalidTokenError(tweets[u'errors'][0]['message'])
        if tweets[u'errors'][0]["code"]==88:
            raise OverflowError(tweets[u'errors'][0]['message'])
        raise Exception(tweets[u'errors'][0]['message'])
    for twit in tweets:
        c.execute('INSERT INTO tweet (tweet_id, created, text, source) VALUES (?, ?, ?, ?)',
            (twit['id'],
            time.mktime(rfc822.parsedate(twit['created_at'])),
            twit['text'],
            twit['source']))
    c.commit()
    return len(tweets)

def print_help(args):
    print( '''
Usage:

    %s <operation> <username>

Operations:

    * init: Create an initial <username>.db file.
    * fetch: Fill in missing tweets for <username>.db
    * fetchAll: Fill in all tweets till that time tweets for <username>.db 
    * fetchRecursive: Fill in missing tweets for <username>.db repeact every 15 minutes

example:
    To gather tweets of '@google' and store in 'google.db'
    To create new DB file
    %s init google
    and then
    %s fetch google

''' % args[0],file=sys.stderr)

def main(*args):
    global c, screen_name
    if len(args) != 3:
        print_help(args)
    elif args[1] == 'init':
        screen_name = args[2]
        try:
            c = connect('%s.db' % screen_name)
            c.execute('CREATE TABLE tweet (tweet_id INTEGER PRIMARY KEY NOT NULL, created INTEGER NOT NULL, text TEXT NOT NULL, source TEXT)')
        except Exception as e:
            print ("Error: There was a problem creating your database: %s" % str(e),file=sys.stderr)
            sys.exit(-1)
    elif args[1] in ('fetch','fetchAll','fetchRecursive'):
        screen_name = args[2]
        try:
            c = connect('%s.db' % screen_name)
        except Exception as e:
            print ("Error: There was a problem opening your database: %s" % str(e),file=sys.stderr)
            sys.exit(-2)
        if args[1] == 'fetchRecursive':
          while True:
            try:
                fetch()
                print ( 'No more tweets found, Sleep 3 minutes')
                time.sleep(180)
            except (KeyboardInterrupt, SystemExit) as e:sys.exit(0)
            except OverflowError as e:
                print ( 'Rate limit exceeded, Sleep 16 minutes',file=sys.stderr)
                time.sleep(1000)
        else:
          if args[1] == 'fetchAll':repeat=True  
          try:
              fetch()
          except Exception as e:
              print( "Error: There was a problem retrieving %s's timeline: %s" % (screen_name, str(e)),file=sys.stderr)
              print ("Error: This may be a temporary failure, wait a bit and try again.",file=sys.stderr)
              sys.exit(-3)
    else:
        print_help(args)

if __name__ == '__main__':
    main(*sys.argv)
