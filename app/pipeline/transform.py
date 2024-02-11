"""
This module provides functions to process data related to albums from the Spotify API.

Note:
    Ensure the DataFrame passed to 'data_quality' contains the expected album information
    with correct column names. Also, make sure the 'albums' parameter provided to 'return_dataframe'
    adheres to the expected format.
"""

# Importing libs
from datetime import datetime

import pandas as pd


def return_dataframe(albums):
    """
    Convert a list of album information into a pandas DataFrame.

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
        "album_id": album_id,
        "album_name": album_name,
        "artist_name": artist_name,
        "album_type": album_type,
        "total_tracks": total_tracks,
        "release_date": release_date,
    }

    spotify_df = pd.DataFrame(
        spotify_dict,
        columns=[
            "album_id",
            "album_name",
            "artist_name",
            "album_type",
            "total_tracks",
            "release_date",
        ],
    )

    return spotify_df


def data_quality(df):
    """
    Check the quality of data in a pandas DataFrame containing album information.

    This function examines the quality of data in the provided DataFrame,
    checking for empty DataFrame, uniqueness of album IDs, and presence of null values.

    Args:
    df (pandas.DataFrame): The DataFrame containing album details.

    Returns:
    bool: True if the data quality checks pass, False otherwise.

    Important:
    - Ensure the DataFrame 'df' contains the expected album information with correct column names.
    - This function modifies the 'release_date' column by adding '-01-01' to entries with only the year.
    - It converts the 'release_date' column to datetime format to facilitate further analysis.

    Raises:
    Exception: If data quality issues are detected (e.g., duplicate album IDs or null values).
    """
    # Check if the DataFrame is empty
    if df.empty:
        print("No albums extracted.")
        return False

    # Check if album IDs are unique
    if pd.Series(df["album_id"]).is_unique:
        pass
    else:
        # Raise an exception if duplicate album IDs are found
        raise Exception("Primary Key exception, data might contain duplicates.")

    # Check for null values in the DataFrame
    if df.isnull().values.any():
        # Raise an exception if null values are found
        raise Exception("Null values found.")

    # Add '-01-01' to entries with only the year
    df["release_date"] = df["release_date"].apply(
        lambda x: x + "-01-01" if len(x) == 4 else x
    )

    # Convert 'release_date' column to datetime format
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
