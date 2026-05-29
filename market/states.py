from indicators.rsi import calculate_rsi

from indicators.momentum import calculate_momentum

from indicators.volatility import detect_volatility

from indicators.volume import detect_volume

from indicators.liquidity import detect_liquidity


# ============================================
# BUILD MARKET STATES
# ============================================

def build_market_states(
    cierres,
    volumenes,
    orderflow
):

    estados = []

    media_volumen = (
        sum(volumenes)
        / len(volumenes)
    )

    # ========================================
    # LOOP THROUGH MARKET DATA
    # ========================================

    for i in range(50, len(cierres)):

        actual = cierres[i]

        anterior = cierres[i - 1]

        pasado = cierres[i - 3]

        volumen_actual = volumenes[i]

        # ====================================
        # PRICE VARIATION
        # ====================================

        variacion = (
            (actual - anterior)
            / anterior
        ) * 100

        # ====================================
        # VOLATILITY
        # ====================================

        volatilidad = detect_volatility(
            variacion
        )

        # ====================================
        # DIRECTION
        # ====================================

        if variacion > 0:

            direccion = "BULLISH"

        elif variacion < 0:

            direccion = "BEARISH"

        else:

            direccion = "SIDEWAYS"

        # ====================================
        # VOLUME STATE
        # ====================================

        volumen_estado = detect_volume(
            volumen_actual,
            media_volumen
        )

        # ====================================
        # MOMENTUM
        # ====================================

        momentum = calculate_momentum(
            actual,
            pasado
        )

        if abs(momentum) > 1:

            momentum_estado = (
                "STRONG_MOMENTUM"
            )

        else:

            momentum_estado = (
                "WEAK_MOMENTUM"
            )

        # ====================================
        # SMA 20
        # ====================================

        sma_20 = (
            sum(cierres[i - 20:i])
            / 20
        )

        if actual > sma_20:

            tendencia = "ABOVE_SMA"

        else:

            tendencia = "BELOW_SMA"

        # ====================================
        # SMA 50
        # ====================================

        sma_50 = (
            sum(cierres[i - 50:i])
            / 50
        )

        if actual > sma_50:

            timeframe_bias = (
                "LONG_TERM_BULLISH"
            )

        else:

            timeframe_bias = (
                "LONG_TERM_BEARISH"
            )

        # ====================================
        # RSI
        # ====================================

        rsi = calculate_rsi(
            cierres[i - 14:i]
        )

        if rsi > 70:

            rsi_estado = "OVERBOUGHT"

        elif rsi < 30:

            rsi_estado = "OVERSOLD"

        else:

            rsi_estado = "NEUTRAL_RSI"

        # ====================================
        # LIQUIDITY
        # ====================================

        liquidez_estado = detect_liquidity(
            actual,
            volumen_actual
        )

        # ====================================
        # MARKET REGIME DETECTION
        # ====================================

        if (
            abs(momentum) > 3
            and volatilidad == "HIGH_VOL"
            and direccion == "BULLISH"
        ):

            market_regime = "BULL_MARKET"

        elif (
            abs(momentum) > 3
            and volatilidad == "HIGH_VOL"
            and direccion == "BEARISH"
        ):

            market_regime = "BEAR_MARKET"

        elif volatilidad == "HIGH_VOL":

            market_regime = (
                "PANIC_VOLATILITY"
            )

        elif (
            momentum_estado
            == "WEAK_MOMENTUM"
        ):

            market_regime = (
                "SIDEWAYS_CHOP"
            )

        else:

            market_regime = "NORMAL_MARKET"

        # ====================================
        # FINAL MARKET STATE
        # ====================================

        estado = (

            f"{market_regime}_"

            f"{volatilidad}_"

            f"{volumen_estado}_"

            f"{momentum_estado}_"

            f"{tendencia}_"

            f"{timeframe_bias}_"

            f"{rsi_estado}_"

            f"{liquidez_estado}_"

            f"{orderflow}_"

            f"{direccion}"
        )

        estados.append(estado)

    return estados