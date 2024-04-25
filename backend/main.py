from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import httpx
from typing import List
from fastapi.encoders import jsonable_encoder
from sql_app.database import SessionLocal, engine
from sql_app.model import Warehouse, TransportationEquipment, TransportationLocation
from sql_app import model
from pydantic import BaseModel


# from .sql_app.model import Warehouse

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
db = SessionLocal()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

id_global = None


# Mount the static directory for serving the HTML file and static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/transportation_planner", response_class=HTMLResponse)
async def transportation_planner(request: Request):
    return templates.TemplateResponse("transportation_planner.html", {"request": request})


@app.get("/warehouse_config", response_class=HTMLResponse)
async def warehouse_config(request: Request):
    
    warehouses = db.query(Warehouse).all()
    warehouse_list = []
    for warehouse in warehouses:
        warehouse_data = {
            "id": warehouse.id,
            "warehouse_user_name": warehouse.warehouse_user_name,
            "warehouse_name": warehouse.warehouse_name,
            "address_lane_1": warehouse.address_lane_1,
            "address_lane_2": warehouse.address_lane_2,
            "state": warehouse.state,
            "city": warehouse.city,
            "zip": warehouse.zip,
        }
        warehouse_list.append(warehouse_data)

    # print(Warehouse)
    return templates.TemplateResponse("warehouse_config.html", {"request": request, "warehouse": warehouse_list})


@app.get("/add_warehouse", response_class=HTMLResponse)
async def add_warehouse(request: Request):
    return templates.TemplateResponse("add_warehouse.html", {"request": request})

@app.get("/update_warehouse/{id}", response_class=HTMLResponse)
async def update_warehouse(request: Request, id: str):

    global id_global
    print(id)
    id_global = id

    all = db.query(Warehouse).all()
    warehouse_list = []
    for warehouse in all:
        warehouse_data = {
            "id": warehouse.id,
            "warehouse_user_name": warehouse.warehouse_user_name,
            "warehouse_name": warehouse.warehouse_name,
            "address_lane_1": warehouse.address_lane_1,
            "address_lane_2": warehouse.address_lane_2,
            "state": warehouse.state,
            "city": warehouse.city,
            "zip": warehouse.zip,
        }
        warehouse_list.append(warehouse_data)
    print(warehouse_list)

    warehouse = db.query(Warehouse).filter(Warehouse.id == id_global).first()
    print("Warehouse",warehouse)
    warehouse_list = []

    warehouse_data = {
        "id": warehouse.id,
        "warehouse_user_name": warehouse.warehouse_user_name,
        "warehouse_name": warehouse.warehouse_name,
        "address_lane_1": warehouse.address_lane_1,
        "address_lane_2": warehouse.address_lane_2,
        "state": warehouse.state,
        "city": warehouse.city,
        "zip": warehouse.zip,
    }
    warehouse_list.append(warehouse_data)

    return templates.TemplateResponse("update_warehouse.html", {"request": request, "warehouse": warehouse_list})


@app.delete("/delete_warehouse/{id}", response_class=HTMLResponse)
async def delete_warehouse(request: Request, id: str):

    print(id)
 
    db.query(Warehouse).filter(Warehouse.id == id).delete()
    db.commit()

    warehouses = db.query(Warehouse).all()
    warehouse_list = []
    for warehouse in warehouses:
        warehouse_data = {
            "id": warehouse.id,
            "warehouse_user_name": warehouse.warehouse_user_name,
            "warehouse_name": warehouse.warehouse_name,
            "address_lane_1": warehouse.address_lane_1,
            "address_lane_2": warehouse.address_lane_2,
            "state": warehouse.state,
            "city": warehouse.city,
            "zip": warehouse.zip,
        }
        warehouse_list.append(warehouse_data)

    # print(Warehouse)
    return templates.TemplateResponse("warehouse_config.html", {"request": request, "warehouse": warehouse_list})


def create_warehouse(data):  
    try:
        new_warehouse = Warehouse(**data)
        db.add(new_warehouse)
        db.commit()
        warehouses = db.query(Warehouse).all()
        warehouse_list = []
        for warehouse in warehouses:
            warehouse_data = {
                "id": warehouse.id,
                "warehouse_user_name": warehouse.warehouse_user_name,
                "warehouse_name": warehouse.warehouse_name,
                "address_lane_1": warehouse.address_lane_1,
                "address_lane_2": warehouse.address_lane_2,
                "state": warehouse.state,
                "city": warehouse.city,
                "zip": warehouse.zip,
            }
            warehouse_list.append(warehouse_data)
        # print(warehouse_list)
        return warehouse_list
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating warehouse: {e}"}
    finally:
        db.close()


def update_warehouse_data(data, id):
    try:
        # Retrieve the warehouse by ID
        warehouse = db.query(Warehouse).filter(Warehouse.id == id).first()
        if warehouse:
            # Update warehouse attributes with new data
            for key, value in data.items():
                setattr(warehouse, key, value)
            db.commit()
            # Return updated warehouse data
            updated_warehouse_data = {
                "id": warehouse.id,
                "warehouse_user_name": warehouse.warehouse_user_name,
                "warehouse_name": warehouse.warehouse_name,
                "address_lane_1": warehouse.address_lane_1,
                "address_lane_2": warehouse.address_lane_2,
                "state": warehouse.state,
                "city": warehouse.city,
                "zip": warehouse.zip,
            }
            return updated_warehouse_data
        else:
            return {"message": "Warehouse not found with the provided ID."}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating warehouse: {e}"}
    finally:
        db.close()


@app.put("/save_warehouse")
async def save_warehouse(
    warehouse_user_name: str = Form(...),
    warehouse_name: str = Form(...),
    address_lane_1: str = Form(...),
    address_lane_2: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    zip: str = Form(...),
    
):
    
    # print(warehouse_user_name, warehouse_name, address_lane_1, address_lane_2, state, city, zip)
    # Create a session
    update_warehouse = {
    "warehouse_user_name": warehouse_user_name,
    "warehouse_name": warehouse_name,
    "address_lane_1": address_lane_1,
    "address_lane_2": address_lane_2,
    "state": state,
    "city": city,
    "zip": zip
}

    global id_global
    id = id_global
    result = update_warehouse_data(update_warehouse,id)
    # print(result)
    return {"message": "Warehouse data updated successfully"}


@app.post("/save_warehouse")
async def save_warehouse(
    warehouse_user_name: str = Form(...),
    warehouse_name: str = Form(...),
    address_lane_1: str = Form(...),
    address_lane_2: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    zip: str = Form(...),
):
    
    # print(warehouse_user_name, warehouse_name, address_lane_1, address_lane_2, state, city, zip)
    # Create a session
    new_warehouse = {
    "warehouse_user_name": warehouse_user_name,
    "warehouse_name": warehouse_name,
    "address_lane_1": address_lane_1,
    "address_lane_2": address_lane_2,
    "state": state,
    "city": city,
    "zip": zip
}
   
    result = create_warehouse(new_warehouse)
    # print(result)
    return {"message": "Warehouse data saved successfully"}


@app.post("/update_warehouse_data")
async def update_warehouse(
    warehouse_user_name: str = Form(...),
    warehouse_name: str = Form(...),
    address_lane_1: str = Form(...),
    address_lane_2: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    zip: str = Form(...),
):
    
    print(warehouse_user_name, warehouse_name, address_lane_1, address_lane_2, state, city, zip)
    # Create a session
    new_warehouse = {
    "warehouse_user_name": warehouse_user_name,
    "warehouse_name": warehouse_name,
    "address_lane_1": address_lane_1,
    "address_lane_2": address_lane_2,
    "state": state,
    "city": city,
    "zip": zip
}
   
    # result = create_warehouse(new_warehouse)
    print("update warehouse")
    # print(result)
    return {"message": "Warehouse data saved successfully"}


@app.get("/trans_equip_config",response_class=HTMLResponse)
async def trans_equip_config(request: Request):

    equipment_list = []
    db = SessionLocal()
    # # Retrieve equipment data from the database
    equipment_records = db.query(TransportationEquipment).all()
 
    
    for equipment in equipment_records:
        equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_license_number": equipment.equipment_license_number,
            "driver_name": equipment.driver_name,
            "driver_license_number": equipment.driver_license_number,
            "equipment_description": equipment.equipment_description,
        }
        equipment_list.append(equipment_data)

    print(equipment_list)

    return templates.TemplateResponse("trans_equip_config.html", {"request": request, "equipment": equipment_list})

@app.get("/add_transport", response_class=HTMLResponse)
async def add_transport_equipment(request: Request):
    return templates.TemplateResponse("add_transport.html", {"request": request})

@app.get("/update_equipment/{id}", response_class=HTMLResponse)
async def update_transport_equipment(request: Request, id: str):

    global id_global
    id_global = id

    equipment_list = []


    equipment = db.query(TransportationEquipment).filter(TransportationEquipment.id == id_global).first()

    equipment_data = {
        "id": equipment.id,
        "equipment_number": equipment.equipment_number,
        "equipment_type": equipment.equipment_type,
        "equipment_license_number": equipment.equipment_license_number,
        "driver_name": equipment.driver_name,
        "driver_license_number": equipment.driver_license_number,
        "equipment_description": equipment.equipment_description,
    }
    equipment_list.append(equipment_data)
    
    return templates.TemplateResponse("update_transport.html", {"request": request, "equipment": equipment_list})


@app.delete("/delete_equipment/{id}", response_class=HTMLResponse)
async def delete_equipment(request: Request, id: str):

    print(id)
 
    db.query(TransportationEquipment).filter(TransportationEquipment.id == id).delete()
    db.commit()

    equipment_list = []
    equipment = db.query(TransportationEquipment).all()
    for equipment in equipment:
        equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_license_number": equipment.equipment_license_number,
            "driver_name": equipment.driver_name,
            "driver_license_number": equipment.driver_license_number,
            "equipment_description": equipment.equipment_description,
        }
        equipment_list.append(equipment_data)

    # print(Warehouse)
    return templates.TemplateResponse("trans_equip_config.html", {"request": request, "warehouse": equipment_list})


@app.post("/save_transport")
async def save_transport(
    equipment_number: str = Form(...),
    equipment_type: str = Form(...),
    equipment_license_number: str = Form(...),
    driver_name: str = Form(...),
    driver_license_number: str = Form(...),
    equipment_description: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    print("hi")
    new_equipment = {
        "equipment_number": equipment_number,
        "equipment_type": equipment_type,
        "equipment_license_number": equipment_license_number,
        "driver_name": driver_name,
        "driver_license_number": driver_license_number,
        "equipment_description": equipment_description,
    }


    print(new_equipment)

    new_equipment = TransportationEquipment(**new_equipment)
    db.add(new_equipment)
    db.commit()


    return {"message": "Equipment added successfully"}


@app.put("/save_transport")
async def save_transport(
    equipment_number: str = Form(...),
    equipment_type: str = Form(...),
    equipment_license_number: str = Form(...),
    driver_name: str = Form(...),
    driver_license_number: str = Form(...),
    equipment_description: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    data = {
        "equipment_number": equipment_number,
        "equipment_type": equipment_type,
        "equipment_license_number": equipment_license_number,
        "driver_name": driver_name,
        "driver_license_number": driver_license_number,
        "equipment_description": equipment_description,
    }


    print(data)
    global id_global
    id = id_global

    try:
        equipment = db.query(TransportationEquipment).filter(TransportationEquipment.id == id).first()
        if equipment:
            for key, value in data.items():
                setattr(equipment, key, value)
            db.commit()

            equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_license_number": equipment.equipment_license_number,
            "driver_name": equipment.driver_name,
            "driver_license_number": equipment.driver_license_number,
            "equipment_description": equipment.equipment_description,
            } 
            return equipment_data
        else:
            return {"message": "Transportation Equipment not found with the provided ID."}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating warehouse: {e}"}
    finally:
        db.close()

        return {"message": "Transporation Equipment data updated successfully"}


@app.get("/trans_location_config",response_class=HTMLResponse)
async def trans_location_config(request: Request):

    transportation_location_list = []
    db = SessionLocal()
    # # Retrieve equipment data from the database
    transportation_location_records= db.query(TransportationLocation).all()
 
    
    for location in transportation_location_records:
        location_data = {
            "id": location.id,
            "index": location.index,
            "villages": location.villages,
            "address": location.address,
        }
        transportation_location_list.append(location_data)

    return templates.TemplateResponse("trans_location_config.html", {"request": request, "location": transportation_location_list})


@app.get("/add_location", response_class=HTMLResponse)
async def add_transport_equipment(request: Request):
    return templates.TemplateResponse("add_location.html", {"request": request})


@app.post("/save_location")
async def save_location(
    index: str = Form(...),
    villages: str = Form(...),
    address: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    print("hi")
    location_data = {
            "index": index,
            "villages": villages,
            "address": address,
        }

    global id_global
    id = id_global

    try:
        location = db.query(TransportationLocation).filter(TransportationLocation.id == id).first()
        if location:
            for key, value in location_data.items():
                setattr(location, key, value)
            db.commit()

            location_data = {
            "index": location.index,
            "villages": location.villages,
            "address": location.address,
            }
            return location_data
        else:
            return {"message": "Transportation Location not found with the provided ID."}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating warehouse: {e}"}
    finally:
        db.close()

        return {"message": "Transporation Location data updated successfully"}



@app.put("/save_location")
async def save_location(
    index: str = Form(...),
    villages: str = Form(...),
    address: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    print("hi")
    location_data = {
            "index": index,
            "villages": villages,
            "address": address,
        }


    print(data)
    global id_global
    id = id_global

    try:
        equipment = db.query(TransportationEquipment).filter(TransportationEquipment.id == id).first()
        if equipment:
            for key, value in data.items():
                setattr(equipment, key, value)
            db.commit()

            equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_license_number": equipment.equipment_license_number,
            "driver_name": equipment.driver_name,
            "driver_license_number": equipment.driver_license_number,
            "equipment_description": equipment.equipment_description,
            } 
            return equipment_data
        else:
            return {"message": "Transportation Equipment not found with the provided ID."}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating warehouse: {e}"}
    finally:
        db.close()

        return {"message": "Transporation Equipment data updated successfully"}






