print("MOMENTUM MODULE LOADED")

def calculate_momentum(current_price, past_price):

    momentum = (
        (current_price - past_price)
        / past_price
    ) * 100

    return momentum