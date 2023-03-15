import pandas as pd
import requests
import datetime as dt
import json

api_url = "http://api.coingecko.com/api/v3/coins/list"

COIN = "ethereum"
PING = "/ping"
COINS_LIST = "/coins/list"
SIMPLE_PRICE = "/simple/price"

COIN_IDS = [
    "ethereum",
    "litecoin",
    "dogecoin",
    "stellar",
    "montero",
    "solana"
]

SP_PARAMS = {
    "ids": ",".join(COIN_IDS),
    "vs_currencies": "usd,btc",
    "include_market_cap": "true",
    "include_24hr_vol": "false",
    "include_24hr_change": "true",
    "include_last_updated_at": "true"
}

# parameters for `COIN_OHLC` payload
OHLC_PARAMS = {
    "id": COIN,
    "vs_currency": "usd",
    "days": 14
}

def print_response(payload, params=None):
    response = requests.get(api_url + payload, params=params)
    data = response.json()

    print(response.status_code)
    print(json.dumps(data, indent=2))

def get_data(payload, params=None):
    response = requests.get(api_url + payload, params=params)
    return response.json()

def create_csv(payload, params=None):
    data = get_data(payload, params)
    dataframe = pd.DataFrame(data)
    csv_file = dataframe.to_csv(dataframe)
    return csv_file

def get_current_prices(payload, params):
    """
    Gets the most recent, current prices of 10 cryptos specified in`COIN_IDS`.
    Simple transformations are done to put the data into the correct shape,
    renaming some columns, and converting Unix timestamp to datetime.
    Args:
        payload (str): A HTTP GET request.
        params (dict): Parameters in the GET request
    Returns:
        dataframe: Cryptocurrency details, ordered by market cap.
    """

    sp_data = get_data(payload=payload, params=params)
    crypto_df = pd.DataFrame(sp_data).transpose().sort_values(by="usd_market_cap", ascending=False).reset_index().rename({"index": "name","usd": "price_in_usd","btc": "price_in_btc"})

    crypto_df['last_updated_at'] = [
        datetime.fromtimestamp(time) for time in crypto_df['last_updated_at']
    ]

    return crypto_df


if __name__ == "__main__":
    coins_data = get_data(payload=COINS_LIST)
    # coin_ids = [coin["id"] for coin in coins_data]

    # Unfortunately, using the above list for the `/simple/price` API gave
    # a JSONDecodeError that I couldn't fix

    # get the required dataframes for crypto prices and Ethereum data
    crypto_df = get_current_prices(payload=SIMPLE_PRICE, params=SP_PARAMS)
    create_csv(payload=COINS_LIST, name="list_of_coins")