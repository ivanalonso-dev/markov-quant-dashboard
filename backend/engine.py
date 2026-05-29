from data.binance_api import get_klines

from market.states import build_market_states

from models.markov_model import (
    build_markov_model,
    predict_next_state
)

from backtesting.backtester import Backtester

# ============================================
# RUN QUANT ENGINE
# ============================================

def run_engine():

    # ========================================
    # GET BINANCE DATA
    # ========================================

    data = get_klines()

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
    # BUILD STATES
    # ========================================

    states = build_market_states(
        closes,
        volumes,
        orderflow
    )

    # ========================================
    # MARKOV MODEL
    # ========================================

    probabilities = build_markov_model(
        states
    )

    # ========================================
    # CURRENT STATE
    # ========================================

    current_state = states[-1]

    predicted_state, confidence = (
        predict_next_state(
            probabilities,
            current_state
        )
    )

    # ========================================
    # SIGNAL
    # ========================================

    if predicted_state:

        if "BULLISH" in predicted_state:

            signal = "BUY"

        elif "BEARISH" in predicted_state:

            signal = "SELL"

        else:

            signal = "HOLD"

    else:

        signal = "HOLD"

    # ========================================
    # BACKTEST
    # ========================================

    backtester = Backtester()

    backtester.run(
        states,
        probabilities,
        closes
    )

    # ========================================
    # WINRATE
    # ========================================

    if backtester.trades > 0:

        winrate = (
            backtester.winning_trades
            / backtester.trades
        ) * 100

    else:

        winrate = 0

    # ========================================
    # SHARPE
    # ========================================

    sharpe = 0

    if len(backtester.returns) > 1:

        import statistics

        avg_return = statistics.mean(
            backtester.returns
        )

        std_return = statistics.stdev(
            backtester.returns
        )

        if std_return != 0:

            sharpe = avg_return / std_return

    # ========================================
    # RETURN DATA
    # ========================================

    return {

        "market_state": current_state,

        "signal": signal,

        "confidence": round(
            confidence,
            2
        ),

        "balance": round(
            backtester.balance,
            2
        ),

        "winrate": round(
            winrate,
            2
        ),

        "sharpe_ratio": round(
            sharpe,
            2
        )
    }