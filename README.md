Replace: 
Access Token key and secret by the users Access Token key and secret
Consumer key and secret by the app's consumer key and secret

in auth_and_Secret.py files for line shown bellow

TweetOuth=Tweetoauth('Access Token key','Access Token Secret','consumer key', 'consumer secret')


Instruction to Execute:
Make sure that you are not under any proxy server and also make sure that internet access is available.

To execute tweetFollow.py

Usage:
in command prompt navigte to directory containing tweetFollow.py(this directory)
python tweetFollow.py <username>

Result:
Strores details of all followers and following of specified users in file named  <username>__follow.log


To execute bmtu.py

Usage:
in command prompt navigte to directory containing bmtu.py(this directory) 


python bmtu.py  <operation> <username>

Operations:

    * init: Create an initial <username>.db file.
    * fetch: Fill in missing tweets for <username>.db

Result:
 Strores the tweets in username.db database


To execute search.py 

Usage:
in command prompt navigte to directory containing search.py(this directory) 

To create DB file
python search.py  init <Search Element>

To fetch into DB
python search.py  fetch <Search Element>

Search Eliment:

	*Searches for Search elements in Twitter
Result:
  Stores result in DB
