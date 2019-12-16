import tweepy
import auth

# Authenticate to Twitter


api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

# Post a tweet
#api.update_status("котик говорит мяу-мяу-мяу")

# Get user data
#user = api.get_user("sanmelisan")
#print("User details:")
#print(user.name)
#print(user.description)
#print(user.location)

# Streaming

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print('Timeout :(')
        return True # Don't kill the stream

stream = tweepy.streaming.Stream(auth, MyStreamListener())   
GEOBOX_GERMANY = [5.077, 47.2982, 15.0403, 54.9039]
GEOBOX_MORDOVIA = [42.5453, 53.9365, 45.9895, 54.7847] 
GEOBOX_MARIEL_1 = [47.7603, 56.0874, 48.9633, 57.0587]
GEOBOX_MARIEL_2 =  [45.903, 56.2615, 47.3916, 56.8848]
GEOBOX_TATAR = [48.5953, 54.7119, 51.4847, 56.0536]

stream.filter(locations=GEOBOX_TATAR) 
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

