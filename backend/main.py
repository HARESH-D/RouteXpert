from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
from typing import List
from fastapi.encoders import jsonable_encoder
from sql_app.database import SessionLocal, engine
from sql_app.model import Warehouse
from sql_app import model
from pydantic import BaseModel
# from .sql_app.model import Warehouse

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
db = SessionLocal()

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

    warehouse = db.query(Warehouse).filter(Warehouse.id == id).first()
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



# def update_data(data, )
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