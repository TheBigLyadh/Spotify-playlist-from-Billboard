import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username= USERNAME,
    )    
)
user_id = sp.current_user()["id"]


date = input("What year you would like to travel to in YYYY-MM-DD format?")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage , "html.parser")
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# sorted_list = sorted(movies_list, key=custom_sort)

# with open("movies.txt", 'w') as file:
#         for item in sorted_list:
#             file.write("%s\n" % item)
