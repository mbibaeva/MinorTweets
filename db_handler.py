import sqlite3

conn = sqlite3.connect("tweets.db") #
cursor = conn.cursor()


def insert_tweets(tweets,language_id):
	for tweet in tweets:
		url = 'https://twitter.com/' + str(tweet.user.screen_name) + '/status/' + tweet.id_str
		#try:
		cursor.execute("INSERT INTO Persons (twitter_id,user,language,created_at,contents,url) VALUES (?,?,?,?,?,?)", 
			[tweet.id_src, tweet.user.screen_name,language_id,tweet.created_at,tweet.text,url])
		conn.commit()
			


def read_by_language(language_id):
	cursor.execute("SELECT * FROM tweets WHERE language_id=?", [(language_id)])
	return cursor.fetchall()