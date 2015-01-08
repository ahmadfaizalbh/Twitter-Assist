# Prerequisites
>## Replace: 
>*    Access Token key and secret by the users Access Token key and secret
>*    Consumer key and secret by the app's consumer key and secret
>
>>####   In auth_and_Secret.py file where line as shown bellow.
>>    TweetOuth=Tweetoauth('Access Token key','Access Token Secret','consumer key', 'consumer secret')
    
>## Instruction to Execute:
>>    Make sure that you are not under any proxy server and also make sure that internet access is available.

# To execute tweetFollow.py
>## Usage:
>>    in command prompt navigte to directory containing tweetFollow.py(this directory)
>
        python tweetFollow.py <username>
>>### Username
>>*	Twitter Username 
>
>## Result:
>>    Strores details of all followers and following of specified users in file named  <username>__follow.log

# To execute bmtu.py
>## Usage:
>>    in command prompt navigte to directory containing bmtu.py(this directory) 
>
        python bmtu.py  <operation> <username>
>>### Operations:
>>*   init: Create an initial <username>.db file.
>>*   fetch: Fill in missing tweets for <username>.db
>
>>### Username
>>*	Twitter Username 
>
>## Result:
>>    Strores the tweets in username.db database


# To execute search.py 
>## Usage:
>>    in command prompt navigte to directory containing search.py(this directory) 
>
        python search.py  <operation> <Search Element>
>>### Operations:
>>*   init: Create an initial <Search Element>.db file.
>>*   fetch: Fill in missing tweets for <Search Element>.db
>
>>### Search Eliment:
>>*   Searches for Search elements in Twitter
>
>##	Example:
>>	To srearch "Cloud Computing"
>>### To create DB file
>>>    python search.py  init "Cloud Computing"
>>### To fetch into DB
>>>    python search.py  fetch "Cloud Computing"
>
>## Result:
>>    Stores result in DB
