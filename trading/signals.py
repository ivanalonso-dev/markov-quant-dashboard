# ============================================
# GENERATE TRADING SIGNAL
# ============================================

def generate_signal(
    predicted_state,
    confidence,
    min_confidence=0.65
):

    if predicted_state is None:

        return "HOLD"

    # ========================================
    # FILTRO DE CONFIANZA
    # ========================================

    if confidence < min_confidence:

        return "HOLD"

    # ========================================
    # BUY
    # ========================================

    if "BULLISH" in predicted_state:

        return "BUY"

    # ========================================
    # SELL
    # ========================================

    elif "BEARISH" in predicted_state:

        return "SELL"

    # ========================================
    # HOLD
    # ========================================

    return "HOLD"