CREATE DATABASE crypto_dwh;

CREATE TABLE crypto_prices (
    coin_id VARCHAR(100),
    symbol VARCHAR(20),
    coin_name VARCHAR(200),
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    last_updated TIMESTAMP
);


--Improvement #1 — Add ETL Load Timestamp to avoid duplicates
ALTER TABLE crypto_prices
ADD COLUMN load_timestamp TIMESTAMP;

--Improvement #2 — Create Primary Key
ALTER TABLE crypto_prices
ADD COLUMN id BIGSERIAL PRIMARY KEY;