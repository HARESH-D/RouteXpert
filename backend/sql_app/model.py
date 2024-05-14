from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Warehouse(Base):

    __tablename__ = "Warehouse"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_user_name = Column(String)
    warehouse_name = Column(String)
    warehouse_prod_types = Column(String)
    address_lane_1 = Column(String)
    address_lane_2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    


class TransportationEquipment(Base):
    __tablename__ = "TransportationEquipment"

    id = Column(Integer, primary_key=True, index=True)
    equipment_number = Column(String)
    equipment_type = Column(String)
    equipment_license_number = Column(String)
    driver_name = Column(String)
    driver_license_number = Column(String)
    equipment_description = Column(String)
    

    
class TransportationLocation(Base):
     
    __tablename__ = "TransportationLocation"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(String)
    villages = Column(String)
    location_demand = Column(String)
    address = Column(String)

class InventoryStatus(Base):

    __tablename__ = "InventoryStatus"

    id = Column(Integer, primary_key=True, index=True)
    invsts = Column(String)
    inv_desc = Column(String)
    inv_shortdesc = Column(String)


    

