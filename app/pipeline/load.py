"""
This module provides functions to interact with PostgreSQL database and perform data operations related to Spotify albums.

Dependencies:
    - pandas: To work with DataFrames.
    - psycopg2: To establish connection with PostgreSQL database.
    - sqlalchemy.create_engine: To create database connection engine.

Important:
    - The functions in this module interact with a PostgreSQL Docker database named 'postgres' running on port 5432.
    - Ensure the PostgreSQL server is running and accessible with the specified credentials.
    - The 'spotify_albums' table structure is predefined with columns:
        - album_id: VARCHAR(100) (Primary Key)
        - album_name: VARCHAR(200) (Not Null)
        - artist_name: VARCHAR(100) (Not Null)
        - album_type: VARCHAR(100)
        - total_tracks: INT
        - release_date: DATE

Note:
    Modify the connection string and table structure as per your PostgreSQL setup and data requirements.
"""

import os

# Importing libs
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")


def dataframe_to_postgres(DataFrame):
    """
    Write DataFrame data to a PostgreSQL Docker database table.

    Args:
    DataFrame (pandas.DataFrame): The DataFrame containing album information to be written to the database.

    Important:
    - This function establishes a connection with the PostgreSQL Docker database.
    - It creates the 'spotify_albums' table if it does not exist.
    - If data already exists in the table, it appends only the new data.
    - Ensure the DataFrame has the correct structure and column names corresponding to the table schema.
    """
    engine = create_engine(
        f"postgresql://{user}:{password}@localhost:{port}/{database}"
    )
    conn = engine.connect()
    conn1 = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port,
    )

    conn1.autocommit = True
    cursor = conn1.cursor()

    # Create table if not exists
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS spotify_albums (
      album_id VARCHAR(100) PRIMARY KEY,
      album_name VARCHAR(200) NOT NULL,
      artist_name VARCHAR(100) NOT NULL,
      album_type VARCHAR(100),
      total_tracks INT,
      release_date DATE
    );
    """

    cursor.execute(sql_create_table)

    # Insert dataframe's data into postgres
    try:
        DataFrame.to_sql("spotify_albums", conn, index=False, if_exists="append")
    except:
        print("Data already exists in the database.")

    conn1.commit()
    conn1.close()
    print("Closed database successfully!")
