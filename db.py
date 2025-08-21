from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///calls.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Negotiation(Base):
    __tablename__ = "negotiation"
    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    load_id = Column(String)
    carrier_rate = Column(Float)
    adjusted_rate = Column(Float)
    round_number = Column(Integer)
    status = Column(String)
    notes = Column(String, default="")

class Load(Base):
    __tablename__ = "loads"
    load_id = Column(String, primary_key=True)
    origin = Column(String)
    destination = Column(String)
    pickup_datetime = Column(String)
    delivery_datetime = Column(String)
    equipment_type = Column(String)
    loadboard_rate = Column(Float)
    notes = Column(String)
    weight = Column(Float)
    num_of_pieces = Column(Integer)
    miles = Column(Float)
    dimensions = Column(String)
    commodity_type = Column(String)
