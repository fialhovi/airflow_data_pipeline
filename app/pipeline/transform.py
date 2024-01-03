# Importing libs
import pandas as pd


def return_dataframe(albums):
  """
  Converts a list of album information into a pandas DataFrame.

  Args:
  albums (list): A list containing dictionaries with album information.

  Returns:
  pandas.DataFrame: A DataFrame containing album details like album ID, name, artist, type,
                    total tracks, and release date.

  Important:
  - This function expects 'albums' to be a list of dictionaries with album information.
  - It extracts specific details from each album dictionary to create a structured DataFrame.
  - Utilizes the pandas library to create and format the DataFrame.
  """
  album_id = []
  album_name = []
  artist_name = []
  album_type = []
  total_tracks = []
  release_date = []

  for i in albums:
    album_id.append(i["id"])
    album_name.append(i["name"])
    artist_name.append(i["artists"][0]["name"])
    album_type.append(i["album_type"])
    total_tracks.append(i["total_tracks"])
    release_date.append(i["release_date"])


  spotify_dict = {
               "album_id" : album_id,
               "album_name": album_name,
               "artist_name": artist_name,
               "album_type" : album_type,
               "total_tracks" : total_tracks,
               "release_date" : release_date
    }

  spotify_df = pd.DataFrame(spotify_dict, columns = ["album_id", "album_name", "artist_name", "album_type", "total_tracks", "release_date"])

  return spotify_df
