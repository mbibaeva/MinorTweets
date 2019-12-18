import tweepy
import re
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['consumer']['key'], cfg['consumer']['secret'])
auth.set_access_token(cfg['access']['token'], cfg['access']['secret'])
api = tweepy.API(auth)

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
    'chechen': ["ПӀ","пӀ", "КӀ", "кӀ", "ЧӀ", "чӀ", "Юь", "юь", "ЦӀ", "цӀ", "ГӀ", "гӀ", "Аь", "аь", "Яь", "яь", "ХӀ", "хӀ", "Къ", "къ"],
    'mari': 'ӸӹҤҥӦӧӰӱӒӓ',
    'mordva': ["йх", "лх", "рх", "Йх", "Лх", "Рх"]
}
coords = { 
    'tatar': "55.8304,49.0661,50km",
    'chechen': "43.3169,45.6815,80km",
    'mari': ["56.6402,47.8839,50km", "56.3294,46.5530,40km"],
    'mordva': ["54.6366,43.2205,50km"]
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
            tweets = api.search(q=l, geocode=place, count=200, since_id=last_created)
        else:
            tweets = api.search(q=l, geocode=place, count=200)
        for tweet in tweets:
            clean = clean_urls(tweet.text)
            if clean not in saved_texts:
                result.append(tweet)
                saved_texts.append(clean)
    return result

def make_blockquote(tweet):
    url = 'https://twitter.com/' + tweet.user.screen_name + '/status/' + tweet.id_str
    bq_tag =    ('<blockquote class="twitter-tweet"><p dir="ltr">' + tweet.text + '</p>&mdash; ' +  tweet.user.name + 
                '(@' + tweet.user.screen_name + ') <a href="' + url + '">' + str(tweet.created_at) + 
                '</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>')
    return bq_tag

def display_tweets(tweets):
    blockquotes = []
    for tweet in tweets:  
        blockquotes.append(make_blockquote(tweet))
    return blockquotes


