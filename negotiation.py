def evaluate_counter_offer(load, carrier_rate, round_number):
    """
    Evaluate the carrier's counter offer.
    Accept if within 90% of the listed loadboard_rate.
    Returns (agreed_rate or None, round_number)
    """
    min_rate = load['loadboard_rate'] * 0.9

    if carrier_rate >= min_rate:
        return carrier_rate, round_number
    return None, round_number