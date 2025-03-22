import pandas as pd
import os

def load_JSON_data(folder_path):
    dataframes = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_json(file_path)
        dataframes.append(df)

    return pd.conact(dataframes, ignore_index=True)


def preprocess_data(data):
    columns_to_read = ["ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name"]

    data = data[columns_to_read]

    data.rename(columns={"ts": "endTime"}, inplace=True)
    data["endTime"] = pd.to_datetime(data["endTime"])

    return data

def save_data(data, file_path="combined_spotify_data.csv"):
    data.to_csv(file_path, index=False)


    