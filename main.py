import os

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=url)
songs_page = response.text

soup = BeautifulSoup(songs_page, "html.parser")

top_100_songs = soup.select(selector="li h3#title-of-a-story")

songs_list = [song.text.strip() for song in top_100_songs]

with open(f"top_100_songs_{date}.txt", "w") as f:
    for sr, song in enumerate(songs_list):
        f.write(f"{sr + 1}. {song}\n")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
tracks = []

for song in songs_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        track = result["tracks"]["items"][0]["uri"]
        tracks.append(track)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

user_id = sp.current_user()["id"]
pl = sp.user_playlist_create(user_id, f"{date} Billbord 100")
sp.playlist_add_items(pl["id"], tracks)
