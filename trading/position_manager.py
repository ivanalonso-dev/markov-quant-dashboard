# ============================================
# POSITION MANAGER
# ============================================

class PositionManager:

    def __init__(self):

        self.in_position = False

        self.position_type = None

        self.entry_price = 0

        self.stop_loss = 0

        self.take_profit = 0

    # ========================================
    # OPEN POSITION
    # ========================================

    def open_position(
        self,
        position_type,
        entry_price,
        stop_loss,
        take_profit
    ):

        self.in_position = True

        self.position_type = position_type

        self.entry_price = entry_price

        self.stop_loss = stop_loss

        self.take_profit = take_profit

        print(
            f"\nOPEN {position_type}"
            f" -> {entry_price:.2f}"
        )

    # ========================================
    # CLOSE POSITION
    # ========================================

    def close_position(self):

        self.in_position = False

        self.position_type = None

        self.entry_price = 0

        self.stop_loss = 0

        self.take_profit = 0

    # ========================================
    # CHECK EXIT
    # ========================================

    def check_exit(
        self,
        current_price,
        predicted_state
    ):

        # ====================================
        # LONG POSITIONS
        # ====================================

        if self.position_type == "LONG":

            # TAKE PROFIT

            if current_price >= self.take_profit:

                return "TAKE_PROFIT"

            # STOP LOSS

            elif current_price <= self.stop_loss:

                return "STOP_LOSS"

            # SIGNAL EXIT

            elif (
                predicted_state
                and "BEARISH" in predicted_state
            ):

                return "SIGNAL_EXIT"

        # ====================================
        # SHORT POSITIONS
        # ====================================

        elif self.position_type == "SHORT":

            # TAKE PROFIT

            if current_price <= self.take_profit:

                return "TAKE_PROFIT"

            # STOP LOSS

            elif current_price >= self.stop_loss:

                return "STOP_LOSS"

            # SIGNAL EXIT

            elif (
                predicted_state
                and "BULLISH" in predicted_state
            ):

                return "SIGNAL_EXIT"

        return None