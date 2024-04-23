from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
from fastapi.encoders import jsonable_encoder
from sql_app.database import SessionLocal, engine
from sql_app.model import Warehouse
from sql_app import model
# from .sql_app.model import Warehouse

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
async def transportation_planner(request: Request):
    return templates.TemplateResponse("warehouse_config.html", {"request": request})

@app.get("/add_warehouse", response_class=HTMLResponse)
async def transportation_planner(request: Request):
    return templates.TemplateResponse("add_warehouse.html", {"request": request})


def create_warehouse(data):
    db = SessionLocal()
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
        print(warehouse_list)
        return {"message": "Warehouse created successfully"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating warehouse: {e}"}
    finally:
        db.close()


def update_data(data, )

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
   
    result = create_warehouse(new_warehouse)
    print(result)
    return {"message": "Warehouse data saved successfully"}