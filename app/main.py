"""
This script performs an ETL (Extract, Transform, Load) process for Spotify's album data.

Dependencies:
    - pipeline.extract: Contains functions to extract data from the Spotify's API.
    - pipeline.transform: Contains functions to transform the extracted data.
    - pipeline.load: Contains functions to load the transformed data into a PostgreSQL Docker database.

Usage:
    - Ensure that the necessary functions are imported from the respective modules.
    - Modify the search term in 'search_for_artist()' function call to search for different artists.
    - Adjust the connection details in 'dataframe_to_postgres()' function call to match your PostgreSQL Docker setup.

Note:
    - This script extracts album data for a specific artist ("Jorge Ben" in the example).
    - It transforms the extracted data into a pandas DataFrame and performs data quality checks.
    - Finally, it loads the cleaned data into a PostgreSQL database table named 'spotify_albums'.

Instructions:
    - Run this script to execute the ETL process for Spotify album data.
    - Make sure to have the necessary dependencies installed and a PostgreSQL Docker database set up.
"""

# Importing libs
from pipeline.extract import (
    get_albums_by_artist,
    get_auth_header,
    get_token,
    search_for_artist,
)
from pipeline.load import dataframe_to_postgres
from pipeline.transform import data_quality, return_dataframe

if __name__ == "__main__":
    # Obtain access token from Spotify API
    token = get_token()
    # Search for the artist and retrieve artist ID
    result = search_for_artist(token, "Jorge Ben")
    artist_id = result["id"]
    # Fetch albums by the artist
    albums = get_albums_by_artist(token, artist_id)

    # Convert album data into a pandas DataFrame
    dataframe = return_dataframe(albums)
    # Perform data quality checks on the DataFrame
    data_quality(dataframe)

    # Load cleaned data into PostgreSQL Docker database
    dataframe_to_postgres(dataframe)

    print("End of ETL.")
