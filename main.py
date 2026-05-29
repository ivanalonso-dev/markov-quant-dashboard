from data.binance_api import get_klines

from market.states import build_market_states

from models.markov_model import (
    build_markov_model,
    predict_next_state
)

from backtesting.backtester import Backtester

# ============================================
# CONFIG
# ============================================

SYMBOL = "BTCUSDT"

INTERVAL = "1h"

LIMIT = 500

# ============================================
# MAIN
# ============================================

def main():

    print("\n====================================")
    print("MARKOV CHAIN TRADING BOT")
    print("QUANTITATIVE FRAMEWORK")
    print("====================================\n")

    # ========================================
    # GET BINANCE DATA
    # ========================================

    data = get_klines(
        symbol=SYMBOL,
        interval=INTERVAL,
        limit=LIMIT
    )

    # ========================================
    # EXTRACT PRICES + VOLUMES
    # ========================================

    closes = []

    volumes = []

    for candle in data:

        close_price = float(candle[4])

        volume = float(candle[5])

        closes.append(close_price)

        volumes.append(volume)

    # ========================================
    # ORDER FLOW
    # ========================================

    orderflow = "BALANCED_ORDERFLOW"

    # ========================================
    # BUILD MARKET STATES
    # ========================================

    states = build_market_states(
        closes,
        volumes,
        orderflow
    )

    print(
        f"TOTAL STATES CREATED:"
        f" {len(states)}"
    )

    # ========================================
    # BUILD MARKOV MODEL
    # ========================================

    probabilities = build_markov_model(
        states
    )

    print(
        f"TOTAL UNIQUE STATES:"
        f" {len(probabilities)}"
    )

    # ========================================
    # CURRENT MARKET STATE
    # ========================================

    current_state = states[-1]

    predicted_state, confidence = (
        predict_next_state(
            probabilities,
            current_state
        )
    )

    print("\n====================================")
    print("CURRENT MARKET STATE")
    print("====================================\n")

    print(current_state)

    print("\n====================================")
    print("PREDICTED NEXT STATE")
    print("====================================\n")

    print(predicted_state)

    print(
        f"\nCONFIDENCE:"
        f" {confidence:.2f}"
    )

    # ========================================
    # RUN BACKTEST
    # ========================================

    backtester = Backtester()

    backtester.run(
        states,
        probabilities,
        closes
    )

    # ========================================
    # RESULTS
    # ========================================

    backtester.results()


# ============================================
# START PROGRAM
# ============================================

if __name__ == "__main__":

    main()