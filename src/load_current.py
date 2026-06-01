import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import text

from config.db_config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

from config.logger import logger

def create_db_engine():

    connection_string = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    engine = create_engine(connection_string)

    return engine

def read_processed_data():

    filepath = "data/processed/crypto_prices_processed.csv"

    df = pd.read_csv(filepath)

    return df

def upsert_coin(row, connection):

    sql = text("""
        INSERT INTO crypto_prices_current
        (
            coin_id,
            symbol,
            coin_name,
            current_price,
            market_cap,
            total_volume,
            last_updated,
            load_timestamp
        )
        VALUES
        (
            :coin_id,
            :symbol,
            :coin_name,
            :current_price,
            :market_cap,
            :total_volume,
            :last_updated,
            :load_timestamp
        )

        ON CONFLICT (coin_id)

        DO UPDATE SET

            symbol = EXCLUDED.symbol,
            coin_name = EXCLUDED.coin_name,
            current_price = EXCLUDED.current_price,
            market_cap = EXCLUDED.market_cap,
            total_volume = EXCLUDED.total_volume,
            last_updated = EXCLUDED.last_updated,
            load_timestamp = EXCLUDED.load_timestamp
    """)
    connection.execute(
            sql,
            {
                "coin_id": row["coin_id"],
                "symbol": row["symbol"],
                "coin_name": row["coin_name"],
                "current_price": row["current_price"],
                "market_cap": row["market_cap"],
                "total_volume": row["total_volume"],
                "last_updated": row["last_updated"],
                "load_timestamp": row["load_timestamp"]
            }
        )       
def load_current():

    logger.info(
        "Starting current table load"
    )

    df = read_processed_data()

    engine = create_db_engine()

    with engine.begin() as connection:

        for _, row in df.iterrows():

            upsert_coin(
                row,
                connection
            )

    logger.info(
        f"Upserted {len(df)} rows"
    )

if __name__ == "__main__":
    load_current()