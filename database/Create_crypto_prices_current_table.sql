CREATE TABLE crypto_prices_current
(
    coin_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(20),
    coin_name VARCHAR(200),
    current_price NUMERIC,
    market_cap NUMERIC,
    total_volume NUMERIC,
    last_updated TIMESTAMP,
    load_timestamp TIMESTAMP
);
