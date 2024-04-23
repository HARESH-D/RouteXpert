from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Warehouse(Base):

    __tablename__ = "Warehouse"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_user_name = Column(String)
    warehouse_name = Column(String)
    address_lane_1 = Column(String)
    address_lane_2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    


class TransportationEquipment(Base):
    __tablename__ = "TransportationEquipment"

    id = Column(Integer, primary_key=True, index=True)
    equip_type = Column(String)
    equip_desc = Column(String)
    

    
class TransportationLocation(Base):
     
    __tablename__ = "TransportationLocation"

    id = Column(Integer, primary_key=True, index=True)
    index = Column(String)
    villages = Column(String)
    address = Column(String)

class InventoryStatus(Base):

    __tablename__ = "InventoryStatus"

    id = Column(Integer, primary_key=True, index=True)
    invsts = Column(String)
    inv_desc = Column(String)
    inv_shortdesc = Column(String)


    

