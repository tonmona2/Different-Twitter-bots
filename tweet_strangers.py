#Todo test and edit tweet to strangers

from flask import Flask, render_template
import tweepy, time, sys
from time import sleep
from random import randint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
from flask import jsonify
from flask import request
import os
import io
import json
from pprint import pprint
import pickle

# counts the number of users to tweet


app = Flask(__name__, template_folder="mytemplate")
list_names = ["@fakeNewsBots"]
list2 = []

# load usernames from database
try:
    with open('data.pkl', 'rb') as f:
        l = pickle.load(f)
        list2 = l

except KeyError:
    pass


try:
    t_consumerkey = ''
    t_secretkey = ''
    access_tokenkey = ''
    access_tokensecret = ''
except KeyError:
    print(
    "You need to set the environment variables: TW_CONSUMERKEY, TW_SECRETKEY, TW_ACCESS_TOKENKEY, TW_TOKENSECRET")
    sys.exit(1)
auth = tweepy.OAuthHandler(t_consumerkey, t_secretkey)
auth.set_access_token(access_tokenkey, access_tokensecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5,
                 retry_errors=5)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_strangers(status)

    def on_error(self, status_code):
        if status_code == 420:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False
        else:
            print(status_code)
            return False


def tweet_strangers(tweet):
    # open file to read hashtags
    user_count = 0
    with open('hashtags.txt') as f:
        for line in f:
            auth = tweepy.OAuthHandler(t_consumerkey, t_secretkey)
            auth.set_access_token(access_tokenkey, access_tokensecret)

            api = tweepy.API(auth)

            search_text = line
            search_number = 2
            search_result = api.search(search_text, rpp=search_number)

            # with io.open('output_tweets.txt', 'a', encoding='utf8') as w:
            #     for tweet in search_result:
            #         w.write('Username:  ' + tweet.author.screen_name + '\n')
            #         w.write("Tweet:  " + tweet.text + "\n")
            # w.close()

    # tweet in the usernames
            for tweet in search_result:
                handle = "@" + tweet.user.screen_name
                print(handle)
                if handle not in list2 and user_count <50:
                    m = handle + " " + "hola! Soy un bot verificando info del sismo. Me puedes confirmar si estos recursos aun se requieren? Grax! #19SRecursos"
                    s = api.update_status(m)
                    nap = randint(1, 60)
                    time.sleep(nap)
                    list2.append(handle)
                    pickle.dump(list2, f)
                    user_count +=1

    f.close()



# Authentication


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['fake'], async=True)

if __name__ == '__main__':
    app.run(debug=True)
