from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
from fastapi.encoders import jsonable_encoder
# from .sql_app.model import Warehouse

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

@app.post("/save_warehouse")
async def save_warehouse(
    warehouse_name: str = Form(...),
    address_lane_1: str = Form(...),
    address_lane_2: str = Form(...),
    state: str = Form(...),
):
    # Process and save form data to the database
    # Insert form_data into the Warehouse table using SQLAlchemy or your ORM of choice
    
    new_warehouse = {
        "warehouse_name": warehouse_name,
        "address_lane_1": address_lane_1,
        "address_lane_2": address_lane_2,
        "state": state,
    }
    print(new_warehouse)
    # db.add(new_warehouse)
    # db.commit()
    
    return {"message": "Warehouse data saved successfully"}
