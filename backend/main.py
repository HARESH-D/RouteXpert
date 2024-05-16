from sql_app.model import Warehouse, TransportationEquipment, TransportationLocation, Driver
from fastapi import FastAPI, Request, Form, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import httpx
from typing import List
from fastapi.encoders import jsonable_encoder
from sql_app.database import SessionLocal, engine
from sql_app import model
from pydantic import BaseModel
import pandas as pd
import json
import numpy as np
import requests
import random
import sys
import matplotlib.pyplot as plt
import time
import plotly.graph_objects as go
from itertools import chain
import openpyxl

BingMapsKey="AtS2Fs-Sm3fm-RPtqb9wDU5VB5cGImY_qIQXbd_Y-cojdSh_RCUDWRj8beBZRm-l"

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
        
    equipment_list = []
    db = SessionLocal()
    # # Retrieve equipment data from the database
    equipment_records = db.query(TransportationEquipment).all()
 
    
    for equipment in equipment_records:
        equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_description": equipment.equipment_description,
        }
        equipment_list.append(equipment_data)

    # print(equipment_list)

    transportation_location_list = []
    db = SessionLocal()
    # # Retrieve equipment data from the database
    transportation_location_records= db.query(TransportationLocation).all()
 
    
    for location in transportation_location_records:
        location_data = {
            "id": location.id,
            "index": location.index,
            "location_demand": location.location_demand,
            "villages": location.address,
            

        }
        transportation_location_list.append(location_data)

        
    warehouses = db.query(Warehouse).all()
    warehouse_list = []
    for warehouse in warehouses:
        warehouse_data = {
            "id": warehouse.id,
            "warehouse_name": warehouse.warehouse_name,
            "warehouse_prod_types": warehouse.warehouse_prod_types,
            "address_lane_2": warehouse.address_lane_2,
        }
        warehouse_list.append(warehouse_data)

    return templates.TemplateResponse("transportation_planner.html", {"request": request, "location": transportation_location_list,"equipment": equipment_list, "warehouse": warehouse_list})



@app.get("/warehouse_config", response_class=HTMLResponse)
async def warehouse_config(request: Request):
    
    warehouses = db.query(Warehouse).all()
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
            "warehouse_prod_types": warehouse.warehouse_prod_types,
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
        "warehouse_prod_types": warehouse.warehouse_prod_types,
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
            "warehouse_prod_types": warehouse.warehouse_prod_types,
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
    warehouse_prod_types: str = Form(...),
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
    "warehouse_prod_types": warehouse_prod_types,
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
    warehouse_prod_types: str = Form(...),
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
    "warehouse_prod_types": warehouse_prod_types,
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
    warehouse_prod_types: str = Form(...),
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
    "warehouse_prod_types": warehouse_prod_types,
    "address_lane_1": address_lane_1,
    "address_lane_2": address_lane_2,
    "state": state,
    "city": city,
    "zip": zip
}
   
    # result = create_warehouse(new_warehouse)
    # print("update warehouse")
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

    # print(equipment_list)

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
            "location_demand": location.location_demand,
            "address": location.address,
            # ""
        }
        transportation_location_list.append(location_data)

    return templates.TemplateResponse("trans_location_config.html", {"request": request, "location": transportation_location_list})


@app.get("/add_location", response_class=HTMLResponse)
async def add_transport_equipment(request: Request):
    return templates.TemplateResponse("add_location.html", {"request": request})

@app.get("/update_location/{id}", response_class=HTMLResponse)
async def update_transport_equipment(request: Request, id: str):

    global id_global
    id_global = id

    equipment_list = []


    equipment = db.query(TransportationLocation).filter(TransportationLocation.id == id).first()
    location_data = {
            "id": equipment.id,
            "index": equipment.index,
            "villages": equipment.villages,
            "location_demand": equipment.location_demand,
            "address": equipment.address,
            }
    equipment_list.append(location_data)
    print(location_data)
    
    return templates.TemplateResponse("update_location.html", {"request": request, "location": equipment_list})


@app.delete("/delete_location/{id}", response_class=HTMLResponse)
async def delete_location(request: Request, id: str):

    print(id)
 
    db.query(TransportationLocation).filter(TransportationLocation.id == id).delete()
    db.commit()

    equipment_list = []
    equipment = db.query(TransportationLocation).all()
    for equipment in equipment:
        equipment_data = {
            "id": equipment.id,
            "index": equipment.index,
            "villages": equipment.villages,
            "location_demand": equipment.location_demand,
            "address": equipment.address,
        }
        equipment_list.append(equipment_data)

    # print(Warehouse)
    return templates.TemplateResponse("trans_location_config.html", {"request": request, "location": equipment_list})


@app.post("/save_location")
async def save_location(
    index: str = Form(...),
    villages: str = Form(...),
    location_demand: str = Form(...),
    address: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    print("hi")
    location_data = {
            "index": index,
            "villages": villages,
            "location_demand": location_demand,
            "address": address,
        }

    new_equipment = TransportationLocation(**location_data)
    db.add(new_equipment)
    db.commit()


    return {"message": "Location added successfully"}


@app.put("/save_location")
async def save_location(
    index: str = Form(...),
    villages: str = Form(...),
    location_demand: str = Form(...),
    address: str = Form(...),
):
    # Process the received data as needed (e.g., save to the database)
    print("hi")
    data = {
            "index": index,
            "villages": villages,
            "location_demand": location_demand,
            "address": address,
        }


    print(data)
    global id_global
    id = id_global

    try:
        equipment = db.query(TransportationLocation).filter(TransportationLocation.id == id).first()
        if equipment:
            for key, value in data.items():
                setattr(equipment, key, value)
            db.commit()

            location_data = {
            "id": equipment.id,
            "index": equipment.index,
            "villages": equipment.villages,
            "address": equipment.address,
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
    




@app.post("/fetch_locations/")
async def fetch_locations(selected_ids: list[int], db: Session = Depends(get_db)):
    try:
        # Query the database for locations based on IDs
        locations = db.query(TransportationLocation).filter(TransportationLocation.id.in_(selected_ids)).all()
        
        # Convert locations to JSON format
        location_data = []
        for location in locations:
            location_data.append({
                "id": location.id,
                "villages": location.villages,
                "location_demand": location.location_demand,
                "address": location.address
            })
        
        return JSONResponse(content=location_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching locations: {e}")


class TransportRequest(BaseModel):
    villages: List[str]
    equipments: List[str]
    warehouses: List[str]

class TransportResponse(BaseModel):
    message: str 
    routes: list



# -------------------------------------------------------------------------------------------------------------------------

@app.post("/transporatation_algorithm", response_model=TransportResponse)
async def transportation_algorithm(request_data: TransportRequest, db: Session = Depends(get_db)):
    # Extract village names from the provided address strings
    village_names_list = []
    for address in request_data.villages:
        # Assuming village name is the first part before the first comma in each address
        village_name = address.split(",")[0].strip()
        village_names_list.append(village_name)

    # Query locations where any village matches the list of village names
    locations = db.query(TransportationLocation).filter(
        TransportationLocation.villages.in_(village_names_list)
    ).all()

    # Convert locations to JSON format
    location_data = []
    for location in locations:
        location_data.append({
            "id": location.id,
            "villages": location.villages,
            "location_demand": location.location_demand,
            "address": location.address
        })



    equipment_list = []
    for address in request_data.equipments:
        # Assuming village name is the first part before the first comma in each address
        equipment = address.split(",")[0].strip()
        equipment_list.append(equipment)


    equipment= db.query(TransportationEquipment).filter(
        TransportationEquipment.equipment_number.in_(equipment_list)
    ).all()


    equipment_xx = equipment
    equipment_list = []
    for equipment in equipment:
        equipment_data = {
            "id": equipment.id,
            "equipment_number": equipment.equipment_number,
            "equipment_type": equipment.equipment_type,
            "equipment_description": equipment.equipment_description,
        }
        equipment_list.append(equipment_data)



    warehouse_list = []
    for address in request_data.warehouses:
        # Assuming village name is the first part before the first comma in each address
        warehouse = address.split(",")[0].strip()
        warehouse_list.append(warehouse)

    print()

    warehouses= db.query(Warehouse).filter(
        Warehouse.warehouse_name.in_(warehouse_list)
    ).all()

    warehouse_list = []
    for warehouse in warehouses:
        warehouse_data = {
            "id": warehouse.id,
            "warehouse_name": warehouse.warehouse_name,
            "warehouse_prod_types": warehouse.warehouse_prod_types,
            "address_lane_2": warehouse.address_lane_2,
        }
        warehouse_list.append(warehouse_data)

    print("Location data",location_data)
    print("equipment data",equipment_list)
    print("warehouse data",warehouse_list)

    location_list = []
    for i in range(len(location_data)):
        location_list.append(location_data[i]['address'])
    
    print("Location list",location_list)

    columns = ["VILLAGES"]
    df = pd.DataFrame(location_list,columns=columns)
    village_coordinates=[]


    for i in range(len(df)):
        locationQuery = df.iloc[i,:].values[0]
        print(locationQuery)
        api = f'http://dev.virtualearth.net/REST/v1/Locations?query={locationQuery}&key={BingMapsKey}'
        response = requests.get(api)
        if response.status_code!=200:
            print(response.json())
            village_coordinates.append("Error fetching location")

        resource = response.json()['resourceSets'][0]['resources']
        if resource == []:
            pass
        else:
            village_coordinates.append(resource[0]['point']['coordinates'])


    

# -------------------------------------------------------------------------------------------------------
    ware_list = []
    for i in range(len(warehouse_list)):
        ware_list.append(warehouse_list[i]['address_lane_2'])
    
    print("Warehouse list",ware_list)

    columns = ["VILLAGES"]
    df = pd.DataFrame(ware_list,columns=columns)
    ware_coordinates=[]

    
    for i in range(len(df)):
        locationQuery = df.iloc[i,:].values[0]
        print(locationQuery)
        api = f'http://dev.virtualearth.net/REST/v1/Locations?query={locationQuery}&key={BingMapsKey}'
        response = requests.get(api)
        if response.status_code!=200:
            print(response.json())
            ware_coordinates.append("Error fetching location")

        resource = response.json()['resourceSets'][0]['resources']
        if resource == []:
            pass
        else:
            ware_coordinates.append(resource[0]['point']['coordinates'])


    print("Number of rows in village address:", df.shape[0])
    print(village_coordinates)
    print("Number of rows in warehouse address:", df.shape[0])
    print(ware_coordinates)


#---------------------------------------------------------------------------------

    df= pd.DataFrame(village_coordinates)
    df2= pd.DataFrame(ware_coordinates)

    locations = []
    for i in range(len(df)):
        lat=df.iloc[i,0]
        long=df.iloc[i,1]
        locations.append({'latitude':lat,'longitude':long})


    def call_api(locations_group,end_group=None):
        if end_group == None:
            end_group = locations_group
        post_req=f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={BingMapsKey}'
        body={"origins": [{"latitude":9.926181981935146, "longitude":78.1428200388285}],'destinations':locations_group,"travelMode": 'Driving'}
        response = requests.post(post_req, json=body)
        if response.status_code!=200:
            print(response.text)
            return [[ float('inf') for i in range(len(locations_group)) ] for j in range(len(locations_group))]
        else:
            data = json.loads(response.text)
            matrix_raw = data['resourceSets'][0]['resources'][0]['results']
            matrix = [ [0 for i in range(len(df))] for j in range(len(df)) ]
            for i in matrix_raw:
                matrix[i['originIndex']][i['destinationIndex']] = i['travelDuration']
            return matrix



    d1_matrix = call_api(locations)
    time_matrix = np.array(d1_matrix)
    np.save('d1_matrix.npy',time_matrix)

    print("length: ",len(time_matrix))
    print(time_matrix)

#----------------------------------------------------------------------------------------------
    
    df= pd.DataFrame(village_coordinates)
    locations = []
    for i in range(len(df)):
        lat=df.iloc[i,0]
        long=df.iloc[i,1]
        locations.append({'latitude':lat,'longitude':long})


    def call_api(locations_group,end_group=None):
        if end_group == None:
            end_group = locations_group
        post_req=f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={BingMapsKey}'
        body={"origins": locations_group,'destinations':end_group,"travelMode": 'Driving'}
        
        response = requests.post(post_req, json=body)
        if response.status_code!=200:
            return [[ float('inf') for i in range(len(locations_group)) ] for j in range(len(locations_group))]
        else:
            data = json.loads(response.text)
            matrix_raw = data['resourceSets'][0]['resources'][0]['results']
            matrix = [ [0 for i in range(len(df))] for j in range(len(df)) ]
            for i in matrix_raw:
                matrix[i['originIndex']][i['destinationIndex']] = i['travelDuration']
            return matrix

    def generate_distance_matrix(locations):
        num_locations = len(locations)
        distance_matrix = [[float('inf') for i in range(num_locations)] for j in range(num_locations)]


        groups = [locations[i:i+49] for i in range(0, num_locations, 49)]


        for i, grouprow in enumerate(groups):
            for j, groupcol in enumerate(groups):
                distance_matrix_group = call_api(grouprow,groupcol)
                start_row = i * 49
                end_row = min(start_row + 49, num_locations)
                start_col = j * 49
                end_col = min(start_col + 49, num_locations)
                for a in range(0,end_row-start_row):
                    for b in range(0,end_col-start_col):
                        # print(i,j,a,b)
                        distance_matrix[start_row+a][start_col+b] = distance_matrix_group[a][b]
                
        return distance_matrix


    d2_matrix = generate_distance_matrix(locations)
    d2_matrix = np.array(d2_matrix)
    np.save('d2_matrix.npy',d2_matrix)

    print("length: ",len(d2_matrix))
    print(d2_matrix)

    #-----------------------------------------------------------------------------------------------

   

    sys.setrecursionlimit(10000000)


    # workbook = openpyxl.load_workbook('village_inputs.xlsx')

    # villages_list = []
    # sheet = workbook["village_inputs"]
    # for row in sheet.iter_rows(values_only=True):
    #     villages_list.append((row[0], row[1]))

    villages_list = village_coordinates

    # Transport location details 
    # villages_list = villages_list[:100]
    max_num_villages = len(villages_list)


    # Warehouse details 
    depot_location = [(9.925485, 78.126581)]
    village_product_demand = [(random.randint(*(0, 5)), random.randint(*(0, 5)), random.randint(*(0, 5))) for _ in range(max_num_villages)]


    # Transport equipment details 
    num_vehicles = len(equipment_list)
    vehicle_max_load = []
    for i in range(len(equipment_list)):
        vehicle_max_load.append(int(equipment_list[i]['equipment_description']))


    vehicles_initial_loc = [(20.5937, 78.9629) for i in range(num_vehicles)]


    if num_vehicles != len(vehicle_max_load):
        print("Error vehicle_max_load !!")

        
    ########################### Time Matix ###########################

    D1 = np.load("d1_matrix.npy").T        #D1 - vehicle/warehouse location to villages
    D2 = np.load("d2_matrix.npy")          #D2[village1] to [village2]
    D3 = D1                         #D3[village][depot]


    #################################################################


    def plot_(plot):
        # Create indices
        indices = range(len(plot))

        # Plot values against indices
        plt.plot(indices, plot)

        # Add labels and title
        plt.xlabel('Episodes')
        plt.ylabel('Rewards')
        plt.title('Episodes vs Rewards Plot')

        # Show the plot
        # plt.show()



    #  initial Order allocation----------------------------------------------------------------
    Q_table = np.zeros((max_num_villages, max_num_villages))
    episilon = 1.0
    temperature = 0.7
    gamma = 0.09  # Discount factor
    alpha = 0.9  # Learning rate
    num_episodes = 500
    plot=[]



    def action_selection(state_village,episilon, decay_rate = 0.99):
        while True:
            a = np.argsort(temp_Q[state_village])[:2]
            if temp_Q[state_village,a[0]]==temp_Q[state_village,a[1]]:
                action = random.choice(a)
            else:
                action = np.argmin(temp_Q[state_village])

            if action != state_village:
                    break

        return action


    def clipped_exp(val):
        return np.exp(np.clip(val, -1000, 1000))

    def softmax(q_values, temperature=temperature):
        exponents = clipped_exp(q_values / temperature)
        return exponents / np.sum(exponents)

    def crude_probabilistic_policy(q_values) -> int:
        probabilities = softmax(q_values)
        return np.random.choice(np.arange(len(q_values)), p=probabilities)

    def action_selection_probability(state_village):
        action = crude_probabilistic_policy(temp_Q[state_village, :])
        if action == state_village:
            action = crude_probabilistic_policy(temp_Q[state_village, :])
        return action

    def soft_state_value_function(q_values, temperature):
        return temperature * np.log( np.mean( clipped_exp(q_values / temperature) ) )

    def pi_maxent(q_values, temperature):
        return clipped_exp( (q_values - soft_state_value_function(q_values, temperature)) / temperature)

    def sql_policy(q_values, temperature):
        pi = pi_maxent(q_values, temperature)
        return crude_probabilistic_policy(pi), pi

    def action_selection_SQL(state_village):
        while True:
            action, pi = sql_policy(temp_Q[state_village,:],temperature=1.)
            if action != state_village:
                break
        return action

    print("villages_list",villages_list)
    print("Initialization Over\n")
    #  initial Order allocation----------------------------------------------------------------




    start_time = time.time()

    for episode in range(num_episodes):

        cumm = 0
        temp_D1 = D1.copy()
        temp_D2 = D2.copy()  
        temp_Q = Q_table.copy()

        finished_tasks = [] 
        vehicle_dist_lst = [0 for _ in range(len(vehicles_initial_loc))]

        vehicle_load_lst = vehicle_max_load.copy()


        vehicle_last_visited_village = [0 for _ in range(len(vehicles_initial_loc))]
        vehicle_visited_village = [[] for _ in range(len(vehicles_initial_loc))]
        

        # print("\nEpisode", episode)


        for vehicle_i in range(len(vehicles_initial_loc)):

            state_village = np.argmin(temp_D1[vehicle_i])       #D1[vehicle_index][state_villagendex]

            vehicle_visited_village[vehicle_i].append(villages_list[state_village])

            reward = D1[vehicle_i][state_village] 

            finished_tasks.append(villages_list[state_village])
            vehicle_dist_lst[vehicle_i] += reward
            vehicle_last_visited_village[vehicle_i] = villages_list[state_village]

            vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

            temp_D2[state_village, :], temp_D2[:, state_village] = np.inf, np.inf
            temp_D1[:, state_village] = np.inf
            temp_Q[:, state_village] = -np.inf 


        while(len(finished_tasks)!=max_num_villages):

            vehicle_i = vehicle_dist_lst.index(min(vehicle_dist_lst)) 
            
            state_village = villages_list.index(vehicle_last_visited_village[vehicle_i])
            

            # action_village = action_selection(state_village, episilon)
            # action_village = action_selection_probability(state_village)
            action_village = action_selection_SQL(state_village)
            
            if sum(village_product_demand[action_village]) > vehicle_load_lst[vehicle_i]:
                # D1[vehicle_i][state_village] + D1[vehicle_i][action_village]
                nearest_depot = np.argmin(D3[state_village])
                
                reward = D3[state_village][nearest_depot] + D3[action_village][nearest_depot]

                
                vehicle_load_lst[vehicle_i] = vehicle_max_load[vehicle_i]
                vehicle_visited_village[vehicle_i].append(villages_list[nearest_depot])
                vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

            else:
                reward = D2[state_village][action_village]
                vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

            Q_table[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(Q_table[action_village], temperature) - Q_table[state_village, action_village])
            temp_Q[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(temp_Q[action_village], temperature) - temp_Q[state_village, action_village])

            temp_D2[action_village, :], temp_D2[:, action_village] = np.inf, np.inf
            temp_D1[:, action_village] = np.inf
            temp_Q[:, action_village] = -np.inf 

            vehicle_dist_lst[vehicle_i]+= reward

            vehicle_last_visited_village[vehicle_i]=villages_list[action_village]
            finished_tasks.append(villages_list[action_village])
            vehicle_visited_village[vehicle_i].append(villages_list[action_village])


        for vehicle_i in range(len(vehicles_initial_loc)):

            state_village = villages_list.index(vehicle_last_visited_village[vehicle_i])

            action_village = action_selection(state_village, episode)
            
            reward = D1[vehicle_i][state_village] 

            Q_table[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(Q_table[action_village], temperature) - Q_table[state_village, action_village])


        plot.append(sum(vehicle_dist_lst))
        moving_avg = np.convolve(plot, np.ones(20)/20, mode='valid')
        
        if len(moving_avg)>100:

            avg_last_to_10 = np.mean(moving_avg[-1:-11:-1])
            avg_10_to_20 = np.mean(moving_avg[-11:-21:-1])

            # Check if any average is below threshold
            threshold = 1336.0
            if abs(avg_10_to_20 - avg_last_to_10)<2:
                break
        

    end_time = time.time()

    # Duration
    duration = end_time - start_time




    # plot_(plot)

    print()
    print("Duration of for loop:", duration, "seconds")
    print("Maximum time spent by a vehicle:", max(vehicle_dist_lst), "mins")
    print("Total time spent by all vehicles:", sum(vehicle_dist_lst), "minssteps")


    window_size =  10
    moving_avg = np.convolve(plot, np.ones(window_size)/window_size, mode='valid')
    # plt.plot(moving_avg)
    # plt.show()

    print("finished_tasks", vehicle_visited_village)
        

    for i in vehicle_visited_village:
        # nearest_depot = np.argmin(D3[ware_coordinates.index(i[0])])
        i.insert(0,ware_coordinates[0])
        i.append(ware_coordinates[0])
        
        print("\n\n\n-------------------------------------------------------------")
        print("i",i)


    print("finished_tasks", vehicle_visited_village)




    # Define your routes

    routes = vehicle_visited_village
    print("\n")
    print("Final Route",routes)


    driver_list = []
    i = 0
    for e in equipment_xx:
        new_driver = {
            "equipment_number": e.equipment_number,
            "equipment_type": e.equipment_type,
            "driver_name": e.driver_name,
            "route": str(routes[i])
        }
        i+=1
        driver_list.append(new_driver)
    print("-------------------------------\n\n")    
    print(driver_list)
    print("\n\n------------------------------")

    new_drivers = Driver(**new_driver)
    db.add(new_drivers)
    db.commit()


    #! Comment out below to visualize
    # # Create a Plotly figure
    # fig = go.Figure()

    # # Add traces for each route with different colors
    # for i, route in enumerate(routes):
    #     fig.add_trace(
    #         go.Scattermapbox(
    #             lat=[location[0] for location in route],
    #             lon=[location[1] for location in route],
    #             mode='lines',
    #             line=go.scattermapbox.Line(width=2, color=['red', 'blue', 'yellow', 'green'][i])
    #         )
    #     )

    # # Add a mapbox layout with Madurai as the center location
    # fig.update_layout(
    #     mapbox_style="open-street-map",
    #     mapbox_center_lat=9.9252,
    #     mapbox_center_lon=78.1198,
    #     mapbox_zoom=5
    # )


    # fig.show()









    #-------------------------------------------------------------------------------------------------------------

    result_message = "Transportation algorithm executed successfully ."
    
    return {"message": result_message, "routes": routes}








