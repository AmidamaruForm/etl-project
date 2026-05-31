import pandas as pd
from sqlalchemy import create_engine

from config.db_config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

def read_processed_data():

    filepath = "data/processed/crypto_prices_processed.csv"

    df = pd.read_csv(filepath)

    return df

def create_db_engine():

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_string)

    return engine

def load_to_database(df, engine):

    df.to_sql(
        name="crypto_prices",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Inserted {len(df)} rows")

def load():

    print("Starting load process")

    df = read_processed_data()

    df = df.rename(
    columns={
        "id": "coin_id",
        "name": "coin_name"
    }
)
    
    engine = create_db_engine()

    load_to_database(df, engine)

    print("Load completed")

if __name__ == "__main__":
    load()