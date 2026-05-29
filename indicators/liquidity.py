def detect_liquidity(price, volume):

    liquidity = price * volume

    if liquidity > 1000000000:
        return "HIGH_LIQUIDITY"

    return "LOW_LIQUIDITY"