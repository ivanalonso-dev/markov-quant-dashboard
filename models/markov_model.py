# ============================================
# BUILD MARKOV MODEL
# ============================================

def build_markov_model(states):

    transitions = {}

    totals = {}

    # ========================================
    # CONTAR TRANSICIONES
    # ========================================

    for i in range(len(states) - 1):

        current_state = states[i]

        next_state = states[i + 1]

        key = (current_state, next_state)

        if key in transitions:

            transitions[key] += 1

        else:

            transitions[key] = 1

        if current_state in totals:

            totals[current_state] += 1

        else:

            totals[current_state] = 1

    # ========================================
    # CALCULAR PROBABILIDADES
    # ========================================

    probabilities = {}

    for key, amount in transitions.items():

        current_state = key[0]

        next_state = key[1]

        probability = amount / totals[current_state]

        if current_state not in probabilities:

            probabilities[current_state] = {}

        probabilities[current_state][next_state] = probability

    return probabilities


# ============================================
# GET NEXT STATE PREDICTION
# ============================================

def predict_next_state(probabilities, current_state):

    if current_state not in probabilities:

        return None, 0

    next_state = max(
        probabilities[current_state],
        key=probabilities[current_state].get
    )

    confidence = probabilities[current_state][next_state]

    return next_state, confidence