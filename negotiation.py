def evaluate_counter_offer(load, carrier_rate, round_number):
    max_rounds = 3
    load_rate = load['loadboard_rate']
    min_acceptable = load_rate * 0.9

    if carrier_rate >= min_acceptable:
        return load_rate, round_number
    else:
        if round_number < max_rounds:
            return None, round_number + 1
        else:
            return None, round_number 
