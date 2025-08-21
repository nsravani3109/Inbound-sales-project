def extract_call_data(load, agreed_rate, round_number):
    """
    Extract relevant information from the call/negotiation.
    Returns a dictionary suitable for logging or reporting.
    """
    call_data = {
        "load_id": load['load_id'],
        "origin": load['origin'],
        "destination": load['destination'],
        "pickup_datetime": load['pickup_datetime'],
        "delivery_datetime": load['delivery_datetime'],
        "equipment_type": load['equipment_type'],
        "agreed_rate": agreed_rate,
        "weight": load.get('weight'),
        "num_of_pieces": load.get('num_of_pieces'),
        "miles": load.get('miles'),
        "dimensions": load.get('dimensions'),
        "commodity_type": load.get('commodity_type'),
        "notes": load.get('notes'),
        "negotiation_rounds": round_number
    }
    return call_data