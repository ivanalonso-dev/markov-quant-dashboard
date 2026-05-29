import statistics

from trading.signals import generate_signal

from trading.risk_management import (
    calculate_stop_loss,
    calculate_take_profit,
    calculate_position_size
)

from trading.position_manager import (
    PositionManager
)

# ============================================
# BACKTESTER
# ============================================

class Backtester:

    def __init__(self, initial_balance=10000):

        self.balance = initial_balance

        self.initial_balance = initial_balance

        self.trades = 0

        self.winning_trades = 0

        self.losing_trades = 0

        self.profit_total = 0

        self.loss_total = 0

        self.returns = []

        self.position_manager = PositionManager()

    # ========================================
    # RUN BACKTEST
    # ========================================

    def run(
        self,
        states,
        probabilities,
        prices
    ):

        for i in range(len(states) - 1):

            current_state = states[i]

            current_price = prices[i + 50]

            next_price = prices[i + 51]

            # ====================================
            # SKIP UNKNOWN STATES
            # ====================================

            if current_state not in probabilities:

                continue

            # ====================================
            # PREDICTION
            # ====================================

            predicted_state = max(
                probabilities[current_state],
                key=probabilities[current_state].get
            )

            confidence = (
                probabilities[current_state][predicted_state]
            )

            # ====================================
            # GENERATE SIGNAL
            # ====================================

            signal = generate_signal(
                predicted_state,
                confidence
            )

            # ====================================
            # OPEN LONG
            # ====================================

            if (
                not self.position_manager.in_position
                and signal == "BUY"
            ):

                stop_loss = calculate_stop_loss(
                    current_price,
                    position_type="LONG"
                )

                take_profit = calculate_take_profit(
                    current_price,
                    position_type="LONG"
                )

                self.position_manager.open_position(
                    "LONG",
                    current_price,
                    stop_loss,
                    take_profit
                )

            # ====================================
            # OPEN SHORT
            # ====================================

            elif (
                not self.position_manager.in_position
                and signal == "SELL"
            ):

                stop_loss = calculate_stop_loss(
                    current_price,
                    position_type="SHORT"
                )

                take_profit = calculate_take_profit(
                    current_price,
                    position_type="SHORT"
                )

                self.position_manager.open_position(
                    "SHORT",
                    current_price,
                    stop_loss,
                    take_profit
                )

            # ====================================
            # CHECK EXITS
            # ====================================

            if self.position_manager.in_position:

                exit_signal = (
                    self.position_manager.check_exit(
                        next_price,
                        predicted_state
                    )
                )

                if exit_signal:

                    self.close_trade(
                        next_price,
                        exit_signal
                    )

    # ========================================
    # CLOSE TRADE
    # ========================================

    def close_trade(
        self,
        exit_price,
        exit_reason
    ):

        position = self.position_manager

        # ====================================
        # LONG
        # ====================================

        if position.position_type == "LONG":

            profit = (
                exit_price - position.entry_price
            )

        # ====================================
        # SHORT
        # ====================================

        elif position.position_type == "SHORT":

            profit = (
                position.entry_price - exit_price
            )

        else:

            return

        # ====================================
        # UPDATE BALANCE
        # ====================================

        self.balance += profit

        self.trades += 1

        self.returns.append(profit)

        # ====================================
        # WIN / LOSS
        # ====================================

        if profit > 0:

            self.winning_trades += 1

            self.profit_total += profit

        else:

            self.losing_trades += 1

            self.loss_total += abs(profit)

        print(
            f"{exit_reason}"
            f" -> Profit: {profit:.2f}"
        )

        # ====================================
        # CLOSE POSITION
        # ====================================

        self.position_manager.close_position()

    # ========================================
    # RESULTS
    # ========================================

    def results(self):

        print("\n================================")
        print("BACKTEST RESULTS")
        print("================================\n")

        print(
            f"Initial Balance:"
            f" {self.initial_balance:.2f}"
        )

        print(
            f"Final Balance:"
            f" {self.balance:.2f}"
        )

        print(f"\nTrades: {self.trades}")

        print(
            f"Winning Trades:"
            f" {self.winning_trades}"
        )

        print(
            f"Losing Trades:"
            f" {self.losing_trades}"
        )

        # ====================================
        # WINRATE
        # ====================================

        if self.trades > 0:

            winrate = (
                self.winning_trades
                / self.trades
            ) * 100

            print(
                f"\nWinrate:"
                f" {winrate:.2f}%"
            )

        # ====================================
        # PROFIT FACTOR
        # ====================================

        if self.loss_total > 0:

            profit_factor = (
                self.profit_total
                / self.loss_total
            )

            print(
                f"Profit Factor:"
                f" {profit_factor:.2f}"
            )

        # ====================================
        # SHARPE RATIO
        # ====================================

        if len(self.returns) > 1:

            avg_return = statistics.mean(
                self.returns
            )

            std_return = statistics.stdev(
                self.returns
            )

            if std_return != 0:

                sharpe = (
                    avg_return
                    / std_return
                )

                print(
                    f"Sharpe Ratio:"
                    f" {sharpe:.2f}"
                )