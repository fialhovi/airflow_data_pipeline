# Importing libs
from dotenv import load_dotenv
import os
import json
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def get_token():
  """
  Requests an access token from the Spotify's API using client credentials.
    
  Returns:
  str: Access token for Spotify's API.

  Important:
  - This function requires 'client_id' and 'client_secret' to be defined before calling.
  - It utilizes the 'requests' library for making HTTP POST requests.
  - 'base64' and 'json' modules are used for encoding and decoding data.
  - The function specifically caters to Spotify's OAuth client credentials flow.

  Raises:
  HTTPError: If the request to Spotify's API fails or returns an error status code.

  Note:
  Ensure 'client_id' and 'client_secret' variables are set correctly before calling this function.
  """
  auth_string = client_id + ":" + client_secret
  auth_bytes = auth_string.encode("utf-8")
  auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

  url = "https://accounts.spotify.com/api/token"
  headers = {
    "Authorization": f"Basic {auth_base64}",
    "Content-Type": "application/x-www-form-urlencoded"
  }

  data = {"grant_type": "client_credentials"}
  result = post(url, headers=headers, data=data)

  json_result = json.loads(result.content)
  token = json_result["access_token"]
  return token

def get_auth_header(token):
  """
  Generates an authorization header for the Spotify's API using the provided token.
    
  Args:
  token (str): The access token obtained from the Spotify's API.

  Returns:
  dict: Authorization header in a dictionary format.

  Note:
  This function specifically generates the 'Authorization' header needed for Spotify's API requests.
  It employs the token obtained from the 'get_token()' function or any other valid access token.
  """
  return {"Authorization": f"Bearer {token}"}


def search_for_artist(token, artist_name):
  """
  Searches for an artist using the Spotify's API.

  Args:
  token (str): The access token obtained from the Spotify's API.
  artist_name (str): The name of the artist to search for.

  Returns:
  dict or None: Information about the first artist found with the provided name. 
                None is returned if no artist is found.

  Important:
  - This function uses the 'get_auth_header()' function to acquire the necessary authorization header.
  - It performs a search for artists based on the given 'artist_name'.
  - The Spotify API endpoint used is '/v1/search'.
  - It fetches only the first matching artist.

  Raises:
  HTTPError: If the request to Spotify's API fails or returns an error status code.

  Note:
  Ensure 'token' is a valid access token obtained from the Spotify's API.
  """
  url = "https://api.spotify.com/v1/search"
  headers = get_auth_header(token)
  query = f"?q={artist_name}&type=artist&limit=1"

  query_url = url + query
  result = get(query_url, headers=headers)
  json_result = json.loads(result.content)["artists"]["items"]

  if len(json_result) == 0:
    print("No artist with this name.")
    return None
  
  return json_result[0]

def get_albums_by_artist(token, artist_id):
  """
  Retrieves albums by a specific artist using the Spotify's API.

  Args:
  token (str): The access token obtained from the Spotify's API.
  artist_id (str): The unique identifier for the artist on Spotify.

  Returns:
  list: A list of albums by the specified artist.

  Important:
  - This function uses the 'get_auth_header()' function to acquire the necessary authorization header.
  - It fetches albums by the artist identified by 'artist_id'.
  - The Spotify API's endpoint used includes the artist's ID to retrieve albums specifically for that artist.
  - The 'country' parameter in the URL specifies a country code for regional results (here, 'BR' for Brazil).

  Raises:
  HTTPError: If the request to Spotify's API fails or returns an error status code.

  Note:
  Ensure 'token' is a valid access token obtained from the Spotify's API.
  """
  url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?country=BR"
  headers = get_auth_header(token)
  result = get(url, headers=headers)
  json_result = json.loads(result.content)["items"]
  return json_result


if __name__ == '__main__':
  token = get_token()
  result = search_for_artist(token, "Jorge Ben")
  artist_id = result["id"]
  albums = get_albums_by_artist(token, artist_id)
  print(albums)

  for idx, album in enumerate(albums):
    print(f"{idx + 1}. {album['name']}")
