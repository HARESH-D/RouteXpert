from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import httpx
from fastapi.encoders import jsonable_encoder

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

