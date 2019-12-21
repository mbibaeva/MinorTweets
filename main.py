from flask import Flask
from flask import render_template, request, redirect, url_for
from jinja2 import Template
from collections import Counter, defaultdict, OrderedDict
import json
import re
import itertools
import http.client, urllib.request, urllib.parse, urllib.error, requests, base64
import pandas as pd

import tweepy
import re
import yaml

import sqlite3

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['consumer']['key'], cfg['consumer']['secret'])
auth.set_access_token(cfg['access']['token'], cfg['access']['secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=False,
    wait_on_rate_limit_notify=True)#, sleep_on_rate_limit=False)

letters = { 
    'tatar': 'ӘәӨөҖҗҢң', 
    'chechen': ["ПӀ","пӀ", "КӀ", "кӀ", "ЧӀ", "чӀ", "Юь", "юь", "хч", "хч", "Оь", "оь", "ЦӀ", "цӀ", "ГӀ", "гӀ", "Аь", "аь", "Яь", "яь", "ХӀ", "хӀ", "Къ", "къ"],
    'mari': 'ӸӹҤҥӦӧӰӱӒӓ',
    'mordva': ["йх", "лх", "рх", "Йх", "Лх", "Рх"],
    'bashkir': "ҒғҘҙҠҡҢңӨөҪҫҺӘә",
    'chuvash': "ӐӑӖӗҪҫӲӳ",
    'buryat': "үӨөҺ"
}
coords = { 
    'tatar': "55.8304,49.0661,100km",
    'chechen': "43.3169,45.6815,100km",
    'mari': ["56.6402,47.8839,90km", "56.3294,46.5530,90km"],
    'bashkir': "54.734773,55.957829,100km",
    'chuvash': "56.138654,47.239894,,90km",
    'buryat': "51.833507,107.584125,100km"
}

def clean_urls(text):
    text = re.sub("http(s)://(\S)+", "", text)
    return text

def collect_tweets(api, place, letters, last_created=None):
    saved_texts = []
    result = []
    print("search started")
    for l in letters:
        if last_created:
            tweets = api.search(q=l, geocode=place, count=1000, since_id=last_created)
        else:
            tweets = api.search(q=l, geocode=place, count=1000)
        for tweet in tweets:
            clean = clean_urls(tweet.text)
            if clean not in saved_texts:
                result.append(tweet)
                saved_texts.append(clean)
    return result

def display_tweets1(tweets):
	blockquotes = []
	for tweet in tweets:  
		url = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str
		blockquotes.append([tweet.text, tweet.user.screen_name, url, str(tweet.created_at)])
	return blockquotes

def display_tweets2(tweets):
    blockquotes = []
    for tweet in tweets:
        blockquotes.append([tweet[4], tweet[2], tweet[6], tweet[5]])
    return blockquotes

conn = sqlite3.connect("tweets.db", check_same_thread = False) #
cursor = conn.cursor()

def insert_tweets(cursor, tweets,language_id):
    inserted = 0
    for tweet in tweets:
        cursor.execute('SELECT * FROM tweets where twitter_id =(?)', (tweet.id_str,))
        if len(cursor.fetchall()) > 0:
            print("Tweet with id", tweet.id_str, "already exists")
        else:
            url = 'https://twitter.com/' + str(tweet.user.screen_name) + '/status/' + tweet.id_str
            try:
                cursor.execute("INSERT INTO tweets (twitter_id,user,language,created_at,contents,url) VALUES (?,?,?,?,?,?)", 
                    [tweet.id_str, tweet.user.screen_name,language_id,tweet.created_at,tweet.text,url])
                conn.commit()
                inserted += 1
            except sqlite3.IntegrityError:
                print("Tweet with id", tweet.id_str, "already exists")
    return inserted

def read_by_language(cursor, language_id):
    cursor.execute("SELECT * FROM tweets WHERE language=?", [(language_id)])
    return cursor.fetchall()

def get_speakers(cursor, language_id):
    cursor.execute("SELECT * FROM languages WHERE id=?", [(language_id)])
    return cursor.fetchall()

app = Flask(__name__)

@app.route('/', methods = ['get'])
def main():
    return render_template('main.html')

@app.route('/tatar', methods = ['post', 'get'])
def display_tatar():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['tatar'], letters['tatar'])
        inserted = insert_tweets(cursor, more_tweets, 1)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 1)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 1)
    return render_template('tatar.html', tweets=blockquotes, speakers=speakers[0][4], news=news)

@app.route('/chechen', methods = ['post', 'get'])
def display_chechen():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['chechen'], letters['chechen'])
        inserted = insert_tweets(cursor, more_tweets, 2)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 2)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 2)
    return render_template('chechen.html', tweets=blockquotes, speakers=speakers[0][4], news=news)

@app.route('/mari', methods = ['post', 'get'])
def display_mari():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['mari'][0], letters['mari'])
        inserted = insert_tweets(cursor, more_tweets, 3)
        even_more_tweets = collect_tweets(api, coords['mari'][1], letters['mari'])
        inserted += insert_tweets(cursor, more_tweets, 3)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 3)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 3)
    return render_template('mari.html', tweets=blockquotes, speakers=speakers[0][4], news=news)

@app.route('/bashkir', methods = ['post', 'get'])
def display_bashkir():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['bashkir'], letters['bashkir'])
        inserted = insert_tweets(cursor, more_tweets, 4)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 4)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 5)
    return render_template('bashkir.html', tweets=blockquotes, speakers=speakers[0][4], news=news) 

@app.route('/chuvash', methods = ['post', 'get'])
def display_chuvash():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['chuvash'], letters['chuvash'])
        inserted = insert_tweets(cursor, more_tweets, 5)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 5)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 5)
    return render_template('chuvash.html', tweets=blockquotes, speakers=speakers[0][4], news=news) 

@app.route('/buryat', methods = ['post', 'get'])
def display_buryat():
    news = 0
    if request.method == "POST":
        more_tweets = collect_tweets(api, coords['buryat'], letters['buryat'])
        inserted = insert_tweets(cursor, more_tweets, 6)
        if inserted > 0:
            news = 2
        else:
            news = 1
    tweets = read_by_language(cursor, 6)
    blockquotes = display_tweets2(tweets)
    speakers = get_speakers(cursor, 6)
    return render_template('buryat.html', tweets=blockquotes, speakers=speakers[0][4], news=news) 

if __name__ == '__main__':
    app.run()