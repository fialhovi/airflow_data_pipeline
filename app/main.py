from pipeline.extract import get_token, get_auth_header, search_for_artist, get_albums_by_artist
from pipeline.transform import return_dataframe
#from pipeline.load import


if __name__ == '__main__':
  token = get_token()
  result = search_for_artist(token, "Jorge Ben")
  artist_id = result["id"]
  albums = get_albums_by_artist(token, artist_id)

  data_frame = return_dataframe(albums)

  