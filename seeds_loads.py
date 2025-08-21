import pandas as pd
from db import SessionLocal, Load

LOADS_CSV = "loads.csv"

def seed_loads():
    df = pd.read_csv(LOADS_CSV)
    session = SessionLocal()
    for _, row in df.iterrows():
        load = Load(
            load_id=row['load_id'],
            origin=row['origin'],
            destination=row['destination'],
            pickup_datetime=row['pickup_datetime'],
            delivery_datetime=row['delivery_datetime'],
            equipment_type=row['equipment_type'],
            loadboard_rate=row['loadboard_rate'],
            notes=row.get('notes', ''),
            weight=row.get('weight', None),
            num_of_pieces=row.get('num_of_pieces', None),
            miles=row.get('miles', None),
            dimensions=row.get('dimensions', None),
            commodity_type=row.get('commodity_type', None)
        )
        session.add(load)
    session.commit()
    session.close()
    print(f"Seeded {len(df)} loads into the database.")
