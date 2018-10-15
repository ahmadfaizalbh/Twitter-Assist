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
>>    Strores details of all followers and following of specified users in file named  &lt;username&gt;__follow.log

# To execute bmtu.py
>## Usage:
>>    in command prompt navigte to directory containing bmtu.py(this directory) 
>
        python bmtu.py  <operation> <username>
>>### Operations:
>>*   init: Create an initial &lt;username&gt;.db file.
>>*   fetch: Fill in missing tweets for &lt;username&gt;.db
>
>>### Username
>>*	Twitter Username 
>
>## Result:
>>    Strores the tweets in &lt;username&gt;.db database


# To execute search.py 
>## Usage:
>>    in command prompt navigte to directory containing search.py(this directory) 
>
        python search.py  <operation> <Search Element>
>>### Operations:
>>*   init: Create an initial &lt;Search Element&gt;.db file.
>>*   fetch: Fill in missing tweets for &lt;Search Element&gt;.db
>
>>### Search Eliment:
>>*   Searches for Search elements in Twitter
>
>##	Example:
>>	To srearch "Cloud Computing"
>>### To create DB file
>>>
    python search.py  init "Cloud Computing"
>>### To fetch into DB
>>>
    python search.py  fetch "Cloud Computing"
>
>## Result:
>>    Stores result in DB

# To execute tweetList.py 
>## Usage:
>>    in command prompt navigte to directory containing tweetList.py(this directory) 
>
       python tweetList.py <operation> <owner username> <slug name>
>>### Operations:
>>* init: Create an initial &lt;owner username&gt;_&lt;slug name&gt;.db file.
>>* fetch: Fill in missing tweets for &lt;owner username&gt;_&lt;slug name&gt;.db
>
>## Example:
>> To get 'Top tech Jobs' list's tweet and store in 'ahmadfaizalbh_top-tech-jobs.db'
>>### To create new DB file
>>>
    python tweetList.py init ahmadfaizalbh top-tech-jobs
>>### To fetch into DB
>>>
    python tweetList.py fetch ahmadfaizalbh top-tech-jobs
>## Result:
>>    Stores result in DB
