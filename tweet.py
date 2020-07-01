import tweepy
import random

consumer_key = "12345"
consumer_secret = "12345"
access_token = "12345"
access_token_secret = "12345"

#random greetings
greetings =  ["Hello", "Bonjour", "Hola", "Hi"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.prev_id = 1

    def on_status(self, tweet):
        api.create_favorite(tweet.id)
        rep = greetings[random.randint(0,3)]+" @"+tweet.user.screen_name+" ! I'm replying to you using a bot. Tweet to you later!  "

        #prevent tweet recursion !important
        if tweet.in_reply_to_status_id != self.previd:
            self.prev_id = tweet.id
            #favorite the mention
            api.create_favorite(tweet.id)
            #replying to mentions
            api.update_status(rep, in_reply_to_status_id = tweet.id)
            
        print(f"{tweet.user.screen_name} >> {tweet.user.name}: {tweet.text}")

    def on_error(self, status):
        print("Error detected")


tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["dddc_10"]) #put your handler here