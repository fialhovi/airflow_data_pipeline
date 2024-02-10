import pandas as pd
from pipeline.extract import (
    get_albums_by_artist,
    get_auth_header,
    get_token,
    search_for_artist,
)
from pipeline.transform import data_quality, return_dataframe

# from pipeline.load import


if __name__ == "__main__":
    token = get_token()
    result = search_for_artist(token, "Jorge Ben")
    artist_id = result["id"]
    albums = get_albums_by_artist(token, artist_id)

    data_frame = return_dataframe(albums)
    data_quality(data_frame)

    print(data_frame.info())
