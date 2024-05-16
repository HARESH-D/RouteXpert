from sqlalchemy.orm import Session
# from .sql_app.database import SessionLocal, engine
import model as model
import database as database
# from .sql_app.model import Warehouse, TransportationEquipment, TransportationLocation


db = database.SessionLocal()

warehouse = db.query(model.Warehouse).all()
print("Warehouse",warehouse)
warehouse_list = []

warehouse_data = {
    "id": warehouse.id,
    "warehouse_user_name": warehouse.warehouse_user_name,
    "warehouse_name": warehouse.warehouse_name,
    "warehouse_prod_types": warehouse.warehouse_prod_types,
    "address_lane_1": warehouse.address_lane_1,
    "address_lane_2": warehouse.address_lane_2,
    "state": warehouse.state,
    "city": warehouse.city,
    "zip": warehouse.zip,
}
warehouse_list.append(warehouse_data)
print(warehouse_list)