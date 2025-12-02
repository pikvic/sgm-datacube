from typing import Annotated

from fastapi import FastAPI, Request, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .stac import search_microsoft


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://datacube.geologyscience.ru",
    "https://datacube.geologyscience.ru",
    "https://localhost",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/assets", StaticFiles(directory="app/templates/map/assets"), name="assets")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/search/landsat", response_class=HTMLResponse)
async def landsat(request: Request):
    return templates.TemplateResponse(request=request, name="search.html", context={"satellite": "landsat", "collection": "landsat-c2-l2"})


@app.get("/search", response_class=HTMLResponse)
async def search_get(request: Request):
    return templates.TemplateResponse(request=request, name="map/index.html")

@app.post("/search", response_class=HTMLResponse)
async def search(
    request: Request, 
    satellite: Annotated[str, Form()],
    min_lat: Annotated[str, Form()], 
    max_lat: Annotated[str, Form()], 
    min_lon: Annotated[str, Form()], 
    max_lon: Annotated[str, Form()],
    start_date: Annotated[str, Form()],
    end_date: Annotated[str, Form()],
):
    print(request)
    if satellite.lower() == "landsat":
        collection = 'landsat-c2-l2'
        bbox = [min_lon, min_lat, max_lon, max_lat]
        time_range = f"{start_date}/{end_date}"
        items = search_microsoft(collection, bbox, time_range)
    elif satellite.lower() == "sentinel-2":
        collection = 'sentinel-2-l2a'
        bbox = [min_lon, min_lat, max_lon, max_lat]
        time_range = f"{start_date}/{end_date}"
        items = search_microsoft(collection, bbox, time_range)

    else:
        items = []

    return templates.TemplateResponse(request=request, name="search_results.html", context={"items": items, "count": len(items)})

