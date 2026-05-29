import requests

def get_klines(symbol="BTCUSDT", interval="1h", limit=500):

    url = (
        f"https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval={interval}&limit={limit}"
    )

    response = requests.get(url)

    return response.json()