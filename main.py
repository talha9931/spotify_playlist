from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
date = input("what year you would like to travel to in YYYY-MM-DD : ")

response= requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response_text = response.text

soup = BeautifulSoup(response_text , "html.parser")
top_100_songs = (soup.findAll("h3", class_="a-no-trucate"))
top_100_songs_list = [songs.getText().strip() for songs in top_100_songs]
print(top_100_songs_list)



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="YOUR_APP_CLIENT_ID",
        client_secret="YOUR_APP_CLIENT_SECRET",
        show_dialog=True,
        cache_path="token.txt",
        username="Your user Name",
    )
)
user_id = sp.current_user()["id"]
print(user_id)
year = date.split("-")[0]
song_uris =[]
for song in top_100_songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
