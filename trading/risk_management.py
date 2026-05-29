# ============================================
# CALCULATE STOP LOSS
# ============================================

def calculate_stop_loss(
    entry_price,
    stop_loss_percent=0.01,
    position_type="LONG"
):

    if position_type == "LONG":

        return entry_price * (
            1 - stop_loss_percent
        )

    elif position_type == "SHORT":

        return entry_price * (
            1 + stop_loss_percent
        )


# ============================================
# CALCULATE TAKE PROFIT
# ============================================

def calculate_take_profit(
    entry_price,
    take_profit_percent=0.02,
    position_type="LONG"
):

    if position_type == "LONG":

        return entry_price * (
            1 + take_profit_percent
        )

    elif position_type == "SHORT":

        return entry_price * (
            1 - take_profit_percent
        )


# ============================================
# POSITION SIZING
# ============================================

def calculate_position_size(
    balance,
    risk_per_trade=0.01
):

    position_size = balance * risk_per_trade

    return position_size


# ============================================
# RISK / REWARD RATIO
# ============================================

def calculate_risk_reward(
    entry_price,
    stop_price,
    take_price
):

    risk = abs(entry_price - stop_price)

    reward = abs(take_price - entry_price)

    if risk == 0:

        return 0

    rr_ratio = reward / risk

    return rr_ratio