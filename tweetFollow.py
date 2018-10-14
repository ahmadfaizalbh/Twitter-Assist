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
    from urllib import urlopen, urlencode, quote_plus 
except ImportError as e:
    from urllib.request import urlopen
    from urllib.parse import urlencode, quote_plus 
from tweetconnect import *
from auth_and_Secret import TweetOuth
def urlencode_utf8(params):
    if hasattr(params, 'items'):
        params = params.items()
    return '&'.join(
        (quote_plus(unicode(k).encode('utf8'), safe='/') + '=' + quote_plus(unicode(v).encode('utf8'), safe='/')
            for k, v in params))


FollowersList=[]
FollowingList=[]
screen_name=None
def print_help(args):
    print('''
Usage:
    %s <Screen_name> 
''' % args[0],file=sys.stderr)
def tweet_friends():
    global FollowingList,screen_name
    follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/friends/ids.json?'+urlencode_utf8({'cursor':-1,'screen_name':screen_name,'count':5000}))
    result=json.loads(follow.decode('utf-8'))
    follow_ids=result[u'ids']
    while result[u'next_cursor']:
        follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/friends/ids.json?'+urlencode_utf8({'cursor':result[u'next_cursor'],'screen_name':screen_name,'count':5000}))
        result=json.loads(follow)
        follow_ids+=result[u'ids']
    follow_list=follow_ids
    while follow_list:
        req_list=str(follow_list[0])
        for i in follow_list[1:100]:
            req_list+=','+str(i)
        lookup=TweetOuth.tweet_req('https://api.twitter.com/1.1/users/lookup.json?user_id='+req_list)
        lookup_result=json.loads(lookup)
        for i in lookup_result:
            FollowingList.append([str(i[u'id']),i[u'name'],i[u'screen_name'],str(i[u'followers_count']),str(i[u'friends_count'])])
        follow_list=follow_list[100:]

def tweet_follower():
    global FollowersList,screen_name
    follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/followers/ids.json?'+urlencode_utf8({'cursor':-1,'screen_name':screen_name,'count':5000}))
    result=json.loads(follow)
    follow_ids=result[u'ids']
    while result[u'next_cursor']:
        follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/followers/ids.json?'+urlencode_utf8({'cursor':result[u'next_cursor'],'screen_name':screen_name,'count':5000}))
        result=json.loads(follow)
        follow_ids+=result[u'ids']
    follow_list=follow_ids
    while follow_list:
        req_list=str(follow_list[0])
        for i in follow_list[1:100]:
            req_list+=','+str(i)
        lookup=TweetOuth.tweet_req('https://api.twitter.com/1.1/users/lookup.json?user_id='+req_list)
        lookup_result=json.loads(lookup)
        for i in lookup_result:
            FollowersList.append([str(i[u'id']),i[u'name'],i[u'screen_name'],str(i[u'followers_count']),str(i[u'friends_count'])])
        follow_list=follow_list[100:]


def Log_File_genrator(fileName):
    global FollowingList,FollowersList,screen_name
    print('Writing to file: '+fileName)
    text_file = open(fileName, "w")
    max_name_len=max([len(i[1]) for i in FollowingList]+[len(i[1]) for i in FollowersList]+[16])+1
    max_sname_len=max([len(i[2]) for i in FollowingList]+[len(i[2]) for i in FollowersList]+[13])+1
    Total_len=(38+max_name_len+max_sname_len)
    text_file.write('FOLLOWING'.rjust(int((Total_len+9)/2))+'\r\n')
    text_file.write('User Id'.ljust(18)+'Name Displayed'.ljust(max_name_len)+'Screen Name'.ljust(max_sname_len)+' Followers Following\r\n')
    text_file.write('='*Total_len+'\r\n')
    for i in FollowingList: 
        text_file.write(i[0].ljust(18)+i[1].ljust(max_name_len).encode( sys.getfilesystemencoding())+i[2].ljust(max_sname_len).encode( sys.getfilesystemencoding())+i[3].rjust(10)+i[4].rjust(10)+'\r\n')
    
    text_file.write('\r\n'+'='*Total_len+'\r\n'+'='*Total_len+'\r\n')
    
    text_file.write('FOLLOWERS'.rjust(int((Total_len+9)/2))+'\r\n')
    text_file.write('User Id'.ljust(18)+'Name Displayed'.ljust(max_name_len)+'Screen Name'.ljust(max_sname_len)+' Followers Following\r\n')
    text_file.write('='*Total_len+'\r\n')
    for i in FollowersList: 
        text_file.write(i[0].ljust(18)+i[1].ljust(max_name_len).encode( sys.getfilesystemencoding())+i[2].ljust(max_sname_len).encode( sys.getfilesystemencoding())+i[3].rjust(10)+i[4].rjust(10)+'\r\n')
    text_file.close()
    print('Sucsess')
    #return search_result
        
def main(*args):
    if len(args) != 2:
        print_help(args)
    else:
        global screen_name
        screen_name = args[1]
        tweet_friends()
        tweet_follower()
        Log_File_genrator(unicode(screen_name+'__follow.log').encode( sys.getfilesystemencoding()))

if __name__ == '__main__':
    main(*sys.argv)
