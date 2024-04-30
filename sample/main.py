from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create FastAPI app
app = FastAPI()

# SQLite Database URL
DATABASE_URL = "sqlite:///./test.db"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM model
Base = declarative_base()

# Define Location model
class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(String)
    longitude = Column(String)

# Create tables in the database (run once)
Base.metadata.create_all(bind=engine)

# Pydantic model for request body
class LocationRequest(BaseModel):
    name: str
    latitude: str
    longitude: str

# API endpoint to create a new location
@app.post("/api/locations/", response_model=Location)
def create_location(location: LocationRequest):
    db = SessionLocal()
    db_location = Location(name=location.name, latitude=location.latitude, longitude=location.longitude)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

# API endpoint to get all locations
@app.get("/api/locations/", response_model=list[Location])
def get_locations():
    db = SessionLocal()
    locations = db.query(Location).all()
    return locations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
