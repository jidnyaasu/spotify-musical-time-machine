from bs4 import BeautifulSoup
import requests


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=url)
songs_page = response.text

soup = BeautifulSoup(songs_page, "html.parser")

top_100_songs = soup.select(selector="li h3#title-of-a-story")

songs_list = [song.text.strip() for song in top_100_songs]
