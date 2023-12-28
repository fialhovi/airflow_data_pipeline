# Imports
import pandas as pd
import requests
import os


# Environment variables
client_id = os.environ['d4e0a233908d42dfb24f83e1231efdd1']
client_secret = os.environ['cc63c76f13dd45ff85bb6ddf5779e243']


# Converting authentication to base64
import base64

string = client_id + ':' + client_secret
string_bytes = string.encode('ascii')

base64_bytes = base64.b64encode(string_bytes)
base64_string = base64_bytes.decode('ascii')


# Request access
url = 'https://accounts.spotify.com/api/token'

headers = {'Authorization': 'Basic ',
           'Content-Type': 'application/x-www-form-urlencoded'}

payload = {'grant_type': 'client_credentials'}

response = requests.request('POST', url = url, headers = headers, data= payload)

access_token = response.json()['access_token']


# Request data
url_data = ''

headers_data = {'Authorization': f'Bearer {access_token}'}

response_data = requests.request('GET', url = url_data, headers = headers_data)

response_data.status_code

pd.json_normalize(response_data.json())