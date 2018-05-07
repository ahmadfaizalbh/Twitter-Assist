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
Search_key = None
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
            print('Requesting tweets newer than %lu' % results[0],file=sys.stderr)
            tweet_count = load_tweets(since_id=results[0])
        if not tweet_count:
            going_up = False
    going_down = True
    while going_down:
        cu = c.cursor()
        cu.execute('SELECT MIN(tweet_id) min_id FROM tweet')
        results = cu.fetchone()
        print('Requesting tweets older than %lu' % results[0],file=sys.stderr)
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
    if type(tweets) == dict and u'errors' in tweets:
        if repeat and tweets[u'errors'][0]["code"]==88:
            print(tweets[u'errors'][0]["message"],file=sys.stderr)
            time.sleep(1000)
            return load_tweets(**kwargs)
        if tweets[u'errors'][0]["code"] in (32,89,99):
            raise InvalidTokenError(tweets[u'errors'][0]['message'])
        if tweets[u'errors'][0]["code"]==88:
            raise OverflowError(tweets[u'errors'][0]['message'])
        raise Exception(tweets[u'errors'][0]['message'])
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
    return len(tweets[u'statuses'])

def print_help(args):
    print('''
Usage:

    %s <operation> <search element>

Operations:

    * init: Create an initial <search element>.db file.
    * fetch: Fill in missing tweets for <search element>.db
    * fetchAll: Fill in all tweets till that time tweets for <search element>.db 
    * fetchRecursive: Fill in missing tweets for <search element>.db repeact every 15 minutes

example:
    To search 'Cloud computing' and store in 'Cloud computing.db'
    To create new DB file
    %s init Cloud_computing
    and then
    %s fetch Cloud computing
''' % (args[0],args[0],args[0]),file=sys.stderr)

def main(*args):
    global c, Search_key,repeat
    if len(args) < 3:
        print_help(args)
    elif args[1] == 'init':
        Search_key = args[2]
        try:
            c = connect('%s.db' % Search_key)
            c.execute('CREATE TABLE tweet (tweet_id INTEGER PRIMARY KEY NOT NULL,user TEXT NOT NULL,screan_name TEXT NOT NULL, description TEXT NOT NULL, created INTEGER NOT NULL, text TEXT NOT NULL, source TEXT)')
        except Exception as e:
            print("Error: There was a problem creating your database: %s" % str(e),file=sys.stderr)
            sys.exit(-1)
    elif args[1] in ('fetch','fetchAll','fetchRecursive'):
        Search_key = args[2]
        for i in args[3:]:
            Search_key += ' ' + i
        try:
            c = connect('%s.db' % Search_key)
        except Exception as e:
            print("Error: There was a problem opening your database: %s" % str(e),file=sys.stderr)
            sys.exit(-2)
        if args[1] == 'fetchRecursive':
          while True:
            try:
                fetch()
                print('No more tweets found, Sleep 3 minutes',file=sys.stderr)
                time.sleep(180)
            except (KeyboardInterrupt, SystemExit) as e:sys.exit(0)
            except OverflowError as e:
                print('Rate limit exceeded, Sleep 16 minutes',file=sys.stderr)
                time.sleep(1000)
        else:
          if args[1] == 'fetchAll':repeat=True  
          try:
              fetch()
          except Exception as e:
              print("Error: There was a problem retrieving %s's timeline: %s" % (Search_key, str(e)),file=sys.stderr)
              print("Error: This may be a temporary failure, wait a bit and try again.",file=sys.stderr)
              sys.exit(-3)
    else:
        print_help(args)

if __name__ == '__main__':
    main(*sys.argv)
