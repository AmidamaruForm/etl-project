import requests
import json
from datetime import datetime


def get_market_data():
    """
    Retrieve cryptocurrency market data from CoinGecko API.
    """

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "per_page": 20,
        "page": 1
    }

    response = requests.get(
        url=url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"API request failed. Status code: {response.status_code}"
        )

    data = response.json()

    if not data:
        raise Exception(
            "No data returned from API"
        )

    return data


def save_raw_data(data):
    """
    Save raw API response into timestamped JSON file.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"crypto_prices_{timestamp}.json"

    filepath = f"data/raw/{filename}"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(f"File saved: {filepath}")


def extract():
    """
    Main extraction workflow.
    """

    print("Starting extraction...")

    data = get_market_data()

    print(f"Retrieved {len(data)} records")

    save_raw_data(data)

    print("Extraction completed.")


if __name__ == "__main__":
    extract()