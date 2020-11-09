import praw
from random import choice as rc

def generate(id, secret, username, password):
	reddit = praw.Reddit(client_id=id,
						client_secret=secret,
						username=username,
						password=password,
						user_agent="script by u/uwu-izzy")
	subreddit = reddit.subreddit("Animemes")
	hot = subreddit.new(limit=25)
	post = rc([(post.title, post.url) for post in hot])
	return post

