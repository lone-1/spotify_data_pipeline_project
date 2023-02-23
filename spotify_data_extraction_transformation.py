import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#add your keys here
client_credentials_manager = SpotifyClientCredentials(client_id="2821dba9f30745a29f4d2a2086e5aec3", client_secret="f7828f168f534b9ca2d8be2ef5672ded")

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF"

playlist_URI =playlist_link.split("/")[-1]
data = sp.playlist_tracks(playlist_URI)

album_list=[]
for row in data['items']:
    album_id= row['track']['album']['id']
    album_name= row['track']['album']['name']
    album_release_date= row['track']['album']['release_date']
    album_total_tracks= row['track']['album']['total_tracks']
    album_external_urls= row['track']['album']['external_urls']['spotify']
    album_element = {'album_id':album_id , 'album_name':album_id , 'album_release_date':album_release_date,
                     'album_total_tracks':album_total_tracks, 'album_external_urls':album_external_urls}
    album_list.append(album_element)
    #print(len(album_list))
    #print(album_list)
    #len(album_list)

artist_list=[]
for row in data['items']:
    for key, value in row.items():
        if key == "track":
            for artist in value['artists']:
                artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                artist_list.append(artist_dict)


song_list = []
for row in data['items']:
    song_id = row['track']['id']
    song_name = row['track']['name']
    song_duration = row['track']['duration_ms']
    song_url = row['track']['external_urls']['spotify']
    song_popularity = row['track']['popularity']
    song_added = row['added_at']
    album_id = row['track']['album']['id']
    artist_id = row['track']['album']['artists'][0]['id']
    song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                    'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                    'artist_id':artist_id
                   }
    song_list.append(song_element)

album_df=pd.DataFrame.from_dict(album_list)
artist_df=pd.DataFrame.from_dict(artist_list)
song_df=pd.DataFrame.from_dict(song_list)

album_df = album_df.drop_duplicates(subset=['album_id'])
artist_df = pd.DataFrame.from_dict(artist_list)
artist_df = artist_df.drop_duplicates(subset=['artist_id'])

album_df['release_date'] = pd.to_datetime(album_df['album_release_date'])
song_df['song_added'] =  pd.to_datetime(song_df['song_added'])

print(album_df)
print(artist_df)
print(song_df)