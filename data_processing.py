import pandas as pd
import os


def load_data(folder_path):
    print(f"📂 Received folder_path: {folder_path}")  # Debug print

    if not os.path.exists(folder_path):
        print(f"❌ Error: File not found at {folder_path}")
        return None 
    
    try:
        data = pd.read_csv(folder_path)
        print(f"✅ Data successfully loaded with {len(data)} rows")
        return data 
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return pd.DataFrame()

def preprocess_data(data):
    columns_to_read = ["endTime", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name"]

    data = data[columns_to_read].copy()

    data.rename(columns={"ts": "endTime"}, inplace=True)
    data.loc[:, "endTime"] = pd.to_datetime(data["endTime"])
    data.fillna("Unknown", inplace=True)

    print("✅ Preprocessing completed")
    
    return data

def save_data(data, folder_path="combined_spotify_data.csv"):
    data.to_csv(folder_path, index=False)

    