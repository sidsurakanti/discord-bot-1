import requests
from random import choice as rc

def get_gif(api_key):
  search_query = "funny anime"
  url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={search_query}&limit=100"
  content = requests.get(url)
  data = content.json()['data']
  gif = rc(data)
  return (gif['images']['original']['url'], gif['url'])
