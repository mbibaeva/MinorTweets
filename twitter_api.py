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

def collect_tweets(api, place, letters):
    saved_texts = []
    result = []
    print("search started")
    for l in letters:
        tweets = api.search(q=l, geocode=place, count=200)
        for tweet in tweets:
            clean = clean_urls(tweet.text)
            if clean not in saved_texts:
                result.append(tweet)
                saved_texts.append(clean)
    print("saved tweets are ", str(len(saved_texts)))
    return result

tatar_res = collect_tweets(api, coords["tatar"], letters["tatar"])
print(len(tatar_res))
print(tatar_res[0].id_str)
print(tatar_res[0].user.screen_name)
print(tatar_res[3].id_str)
print(tatar_res[3].user.screen_name)

url = 'https://twitter.com/' + str(tweet.name) + '/status/' + tweet.id_str

