import tweepy
import re
#import auth

# Authenticate to Twitter


api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=False,
    wait_on_rate_limit_notify=True)#, sleep_on_rate_limit=False)

# Post a tweet
#api.update_status("котик говорит мяу-мяу-мяу")

# Get user data
#user = api.get_user("sanmelisan")
#print("User details:")
#print(user.name)
#print(user.description)
#print(user.location)
#print(api.geo_id(id="219a76ffddcfd1c6"))

#api.search(" ", geocode="1a6c4d96a65b6c9b") # Mordor
#martweets = api.search("ӓ", geocode="219a76ffddcfd1c6", result_type="mixed", count=20)
joshkar_ola = "56.6402,47.8839,50km"
kozmodem = "56.3294,46.5530,50km"
kazan = "55.8304,49.0661,50km"
mikryak = "56.2028,46.2413,15km"
groznyj = "43.3169,45.6815,80km"
makhachakala = "42.9666,47.5126,30km"
ufa = "54.7388,55.9721,40km"
qamishli = "37.0549,41.2282,40km"
yakut = "66.7613,124.1238,400km"
cheboxar = "56.1168,47.2628,50km"

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

#mari_letters = 
#martweets = api.search(q='', geocode=kazan, count=2000)
#seen_tweets = []
#for tweet in martweets:
    #print(tweet.user.name, ":", tweet.text)
    #if tweet.text not in seen_tweets:
    #    print(tweet.created_at, ":", tweet.text)
    #    seen_tweets.append(tweet.text)
    #print("\n")
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

chechen = collect_tweets(api, groznyj, letters["chechen"])
print(len(chechen))
for x in chechen[:20]:
    print(x.created_at, ":", x.text)


tatars = collect_tweets(api, kazan, tatar_letters)
print(len(tatars))
#for x in tatars[:20]:
#    print(x.created_at, ":", x.text)

def is_Mari(text): 
    uml = re.findall('ӹ|ӓ|ӱ', text)
    if len(uml) > 0:
        return True
    else:
        return False

# Streaming

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if is_Mari(status.text):
            print("Mari tweet: ")
            print(status)
        else:
            print("Not Mari: ")
            print(status)

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout............')
        return True # Don't kill the stream

stream = tweepy.streaming.Stream(auth, MyStreamListener())   
GEOBOX_GERMANY = [5.077, 47.2982, 15.0403, 54.9039]
GEOBOX_MORDOVIA = [42.5453, 53.9365, 45.9895, 54.7847] 
GEOBOX_MARIEL = [46.2272043349,56.1000552794,49.0506906631,56.9304162493]
GEOBOX_MARIEL_1 = [47.7603, 56.0874, 48.9633, 57.0587]
GEOBOX_MARIEL_2 =  [45.903, 56.2615, 47.3916, 56.8848]
GEOBOX_TATAR = [48.5953, 54.7119, 51.4847, 56.0536]

stream.filter(locations=GEOBOX_MARIEL) 
#stream.filter(locations=[42.5453,53.9365,45.9895,54.7847])

marr = api.reverse_geocode(lat=53.9365, long=42.5453, accuracy=1, granularity='city', max_results=5)
print(len(marr))
for x in marr:
	print('>>>')
	print(x.full_name)
	print(x.id)
	if len(x.contained_within) > 0:
		print(x.contained_within[0].full_name)

print(api.geo_id(id="1a6c4d96a65b6c9b"))
#myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)



#class LangFinder():
#	def __init__():
#		self.locations = {
#			'mordva': [42.5453,53.9365,45.9895,54.7847], 'mari1': [47.7603,56.0874,48.9633,57.0587],
#			'mari2': [45.903,56.2615,47.3916,56.8848], 'tatar': [48.5953,54.7119,51.4847,56.0536]}
#
#	def find_locals(api, count, location):
#		new_tweets = api.search(count=count, geo max_id=str(last_id - 1))
#
#	def on_status(self, status):
#        print(status.text)
#    def on_error(self, status_code):
#        if status_code == 420:
#            #returning False in on_error disconnects the stream
#            return False

