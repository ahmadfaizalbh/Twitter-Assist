import oauth2x as oauth


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

        #self.consumer.key='i8UBkayvyDbBGKABGBTAbA'
        #self.consumer.secret='tkocm4ejnoMBCt7qy03R8P5lmHV75vUl0ZOQiuIgo'
        #customer Access Token Key and secret
        #self.AccessToken.key='786022-ML65piqV7vsZ58l7fx4lM91VZ2qvVXnVLm6sPk3N2Ik'
        #self.AccessToken.secret='9DDprtzfCBLr8JW1wwZMmcTkY96zgNqSyBkOZqobHo'
        
        

    def tweet_req(self,url, http_method="GET", post_body=None, http_headers=None):
        consumer = oauth.Consumer(key=self.consumer.key,secret=self.consumer.secret)#change your 'Consumer key' and 'Consumer secret' with your apps 'Consumer key' and 'Consumer secret'
        token = oauth.Token(key=self.AccessToken.key, secret=self.AccessToken.secret)
        client = oauth.Client(consumer, token)
        resp, content = client.request(
            url,
            method=http_method,
            body=post_body,
            headers=http_headers,
            force_auth_header=True
        )
        return content

 
