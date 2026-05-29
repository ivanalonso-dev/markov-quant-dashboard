from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

import requests

from backend.engine import run_engine

app = FastAPI()

# ============================================
# CORS
# ============================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ============================================
# ROOT
# ============================================

@app.get("/")

def root():

    return {

        "message": "Markov Quant API Running"
    }

# ============================================
# MARKET DATA
# ============================================

@app.get("/market-data")

def market_data():

    return run_engine()

# ============================================
# BTC PRICE HISTORY
# ============================================

@app.get("/btc-history")

def btc_history():

    url = (
        "https://api.binance.com/api/v3/klines"
        "?symbol=BTCUSDT"
        "&interval=1h"
        "&limit=100"
    )

    response = requests.get(url)

    data = response.json()

    prices = []

    for candle in data:

        prices.append({

            "time": candle[0] // 1000,

            "value": float(candle[4])
        })

    return prices