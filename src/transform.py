import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from config.logger import logger

def get_latest_raw_file():
    raw_folder = Path("data/raw")

    files = list(raw_folder.glob("*.json"))

    if not files:
        logger.error("No raw files found")
        raise Exception("No raw files found")

    latest_file = max(files, key=lambda file: file.stat().st_mtime)

    return latest_file

def read_raw_data(filepath):

    with open(filepath, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data

def create_dataframe(data):

    df = pd.DataFrame(data)

    return df

def transform_data(df):

    selected_columns = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "last_updated"
    ]

    transformed_df = df[selected_columns]

    transformed_df = transformed_df.rename(
        columns={
            "id": "coin_id",
            "name": "coin_name"
        }
    )

    transformed_df["load_timestamp"] = datetime.now()

    
    return transformed_df

def save_processed_data(df):

    output_file = "data/processed/crypto_prices_processed.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(f"Processed data saved: {output_file}")

def transform():

    latest_file = get_latest_raw_file()

    logger.info(f"Using raw file: {latest_file}")

    raw_data = read_raw_data(latest_file)

    df = create_dataframe(raw_data)

    transformed_df = transform_data(df)

    save_processed_data(transformed_df)

    logger.info(f"Processed {len(transformed_df)} rows")

if __name__ == "__main__":
    transform()