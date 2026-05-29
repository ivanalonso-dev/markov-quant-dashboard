def detect_volume(current_volume, average_volume):

    if current_volume > average_volume:
        return "HIGH_VOLUME"

    return "LOW_VOLUME"