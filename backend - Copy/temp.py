from sqlalchemy.orm import Session
from sql_app.database import SessionLocal
from sql_app.model import Warehouse

# Create a database session
db = SessionLocal()

# Query all Warehouse records from the database
warehouses = db.query(Warehouse).all()

# Process each Warehouse object
warehouse_list = []
for warehouse in warehouses:
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

# Print the list of warehouse data
print(warehouse_list)
