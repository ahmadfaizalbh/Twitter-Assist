import oauth2 as oauth


class key_secret():
    def __init__(self,key,secret):
        self.key=key
        self.secret=secret
        
class Tweetoauth():
    def __init__(self,Access_key,Access_secret,consumer_key,consumer_secret):
        #app consumer key and secret
        self.consumer=key_secret(consumer_key,consumer_secret)
        #customer Access Token Key and secret
        self.AccessToken=key_secret(Access_key,Access_secret)

        

    def tweet_req(self,url, http_method="GET", post_body="", http_headers=""):
        consumer = oauth.Consumer(key=self.consumer.key,secret=self.consumer.secret)#change your 'Consumer key' and 'Consumer secret' with your apps 'Consumer key' and 'Consumer secret'
        token = oauth.Token(key=self.AccessToken.key, secret=self.AccessToken.secret)
        client = oauth.Client(consumer, token)
        resp, content = client.request(
            url,
            method=http_method,
            body=post_body,
            headers=http_headers,
        )
        return content

 
