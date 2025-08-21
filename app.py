from fastapi import FastAPI
from pydantic import BaseModel
from fmca_api import verify_mc_number
from load_manager import LoadManager
from negotiation import evaluate_counter_offer
from extract_data import extract_call_data
from classify import classify_outcome, classify_sentiment
from db import SessionLocal, Negotiation, Load
import uuid

app = FastAPI()
load_manager = LoadManager()

class MCRequest(BaseModel):
    mc_number: str

class LoadSearchRequest(BaseModel):
    origin: str = None
    destination: str = None
    equipment_type: str = None
    weight: float = None
    commodity_type: str = None
    pickup_datetime: str = None
    delivery_datetime: str = None
    loadboard_rate: float = None
    num_of_pieces: int = None
    miles: float = None
    dimensions: str = None
    notes: str = None

class CounterOfferRequest(BaseModel):
    session_id: str
    load_id: str
    carrier_rate: float
    round_number: int = 1

class LoadInsertRequest(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: str
    delivery_datetime: str
    equipment_type: str
    loadboard_rate: float
    notes: str = None
    weight: float = None
    num_of_pieces: int = None
    miles: float = None
    dimensions: str = None
    commodity_type: str = None

@app.post("/validate_mc")
def validate_mc(request: MCRequest):
    is_verified, insurance_ok = verify_mc_number(request.mc_number)
    return {
        "is_verified": is_verified,
        "insurance_ok": insurance_ok,
        "status": "eligible" if is_verified and insurance_ok else "ineligible",
        "session_id": str(uuid.uuid4())
    }

@app.post("/create_load")
def create_load(request: LoadCreateRequest):
    db = SessionLocal()
    # Check if load already exists
    existing = db.query(Load).filter_by(load_id=request.load_id).first()
    if existing:
        db.close()
        return {"error": f"Load {request.load_id} already exists."}

    load = Load(
        load_id=request.load_id,
        origin=request.origin,
        destination=request.destination,
        pickup_datetime=request.pickup_datetime,
        delivery_datetime=request.delivery_datetime,
        equipment_type=request.equipment_type,
        loadboard_rate=request.loadboard_rate,
        notes=request.notes,
        weight=request.weight,
        num_of_pieces=request.num_of_pieces,
        miles=request.miles,
        dimensions=request.dimensions,
        commodity_type=request.commodity_type
    )
    db.add(load)
    db.commit()
    db.close()
    return {"message": f"Load {request.load_id} created successfully."}

@app.post("/search_loads")
def search_loads_endpoint(request: LoadSearchRequest):
    results = load_manager.search_loads(**request.dict())
    return {"loads": results}

@app.post("/evaluate_counter_offer")
def evaluate_counter_offer_endpoint(request: CounterOfferRequest):
    try:
        db = SessionLocal()
        # Query the load properly
        load = db.query(Load).filter_by(load_id=request.load_id).first()
        if not load:
            db.close()
            return {"error": f"Load {request.load_id} not found"}

        # Convert Load object to dict
        load_dict = {c.name: getattr(load, c.name) for c in load.__table__.columns}

        # Evaluate counter offer
        agreed_rate, round_number = evaluate_counter_offer(load_dict, request.carrier_rate, request.round_number)

        # Save negotiation
        db.add(Negotiation(
            session_id=request.session_id,
            load_id=load.load_id,
            carrier_rate=request.carrier_rate,
            adjusted_rate=agreed_rate if agreed_rate else None,
            round_number=round_number,
            status="accepted" if agreed_rate else "rejected"
        ))
        db.commit()
        db.close()

        if agreed_rate:
            call_data = extract_call_data(load_dict, agreed_rate, round_number)
            outcome = classify_outcome(call_data)
            sentiment = classify_sentiment(call_data)
            return {
                "agreed_rate": agreed_rate,
                "round_number": round_number,
                "call_data": call_data,
                "outcome": outcome,
                "sentiment": sentiment,
                "next_action": "transfer_to_rep"
            }
        else:
            return {"message": "Counter offer rejected", "next_action": "negotiate_again"}
    except Exception as e:
        return {"error": str(e)}

