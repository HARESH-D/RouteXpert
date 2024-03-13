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

# @app.get("/geocode/{location}", response_model=dict)
# async def geocode_location(location: str):
#     # Use Bing Maps Location API to get the coordinates of the location.
#     bing_maps_key = "AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk"
#     geocode_request = f"http://dev.virtualearth.net/REST/v1/Locations/{location}?key={bing_maps_key}"

#     async with httpx.AsyncClient() as client:
#         response = await client.get(geocode_request)

#         if response.status_code == 200:
#             data = response.json()
#             coordinates = data["resourceSets"][0]["resources"][0]["point"]["coordinates"]
#             result = {"latitude": coordinates[0], "longitude": coordinates[1]}
#             return jsonable_encoder(result)
#         else:
#             return {"error": f"Error geocoding location: {response.text}"}
