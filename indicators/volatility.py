def detect_volatility(variation):

    if abs(variation) > 1:
        return "HIGH_VOL"

    return "LOW_VOL"