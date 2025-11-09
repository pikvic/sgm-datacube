from fastapi import APIRouter
from pydantic import BaseModel
import pystac
import planetary_computer
from app.stac import search_microsoft, search_roscosmos

COLLECTIONS = [
    {
        "name": "landsat-c2-l2",
        "description": "Landsat Collection 2 Level-2 Science Products, consisting of atmospherically corrected surface reflectance and surface temperature image data. Collection 2 Level-2 Science Products are available from August 22, 1982 to present. This dataset represents the global archive of Level-2 data from Landsat Collection 2 acquired by the Thematic Mapper onboard Landsat 4 and 5, the Enhanced Thematic Mapper onboard Landsat 7, and the Operatational Land Imager and Thermal Infrared Sensor onboard Landsat 8 and 9. Images are stored in cloud-optimized GeoTIFF format.",
        "source": "Microsoft Planetary Computer",
        "provider": "NASA, USGS",
        "search": search_microsoft
    },
    {
        "name": "modis-09A1-061",
        "description": "The Moderate Resolution Imaging Spectroradiometer (MODIS) 09A1 Version 6.1 product provides an estimate of the surface spectral reflectance of MODIS Bands 1 through 7 corrected for atmospheric conditions such as gasses, aerosols, and Rayleigh scattering. Along with the seven 500 meter (m) reflectance bands are two quality layers and four observation bands. For each pixel, a value is selected from all the acquisitions within the 8-day composite period. The criteria for the pixel choice include cloud and solar zenith. When several acquisitions meet the criteria the pixel with the minimum channel 3 (blue) value is used.",
        "source": "Microsoft Planetary Computer",
        "provider": "NASA LP DAAC at the USGS EROS Center",
        "search": search_microsoft
    },
    {
        "name": "roscosmos-opendata.MM",
        "description": "Глобальные мозайки. Солнечно-синхронная метеорологическая космическая система Метеор-М. По состоянию на 2025 год состоит из двух космических аппаратов. Радиометр МСУ-МР производит непрерывное сканирование.",
        "source": "Роскосмос",
        "provider": "Роскосмос",
        "search": search_roscosmos
    },
    
]

# Declare models for API
# - SearchResult for Nominatim
# - SearchResult for STAC
# - SearchParams for STAC

# Declare routes
# - Nominatim search
# - stac search

# Make functions
# - nominatim search
# - stac search


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class SearchParams(BaseModel):
    start: str
    end: str
    lat1: str
    lat2: str
    lon1: str
    lon2: str

router = APIRouter(prefix="/api")


@router.get("/stac/", tags=["users"])
async def read_stac():
    item_url = "https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2/items/LC09_L2SP_114030_20250623_02_T1"

    # Load the individual item metadata and sign the assets
    item = pystac.Item.from_file(item_url)

    signed_item = planetary_computer.sign(item)
    
    # Open one of the data assets (other asset keys to use: 'red', 'blue', 'drad', 'emis', 'emsd', 'trad', 'urad', 'atran', 'cdist', 'green', 'nir08', 'lwir11', 'swir16', 'swir22', 'coastal', 'qa_pixel', 'qa_radsat', 'qa_aerosol')
    preview = signed_item.assets["rendered_preview"].href
    items = [{"name": key, "preview": preview, "href": value.href} for key, value in signed_item.assets.items() if ".TIF" in value.href]
    
    return items

@router.post("/collections/{name}/results")
async def search(name: str, params: SearchParams):
    bbox = [params.lon1, params.lat1, params.lon2, params.lat2]
    time_range = f"{params.start}/{params.end}"
    collection = [col for col in COLLECTIONS if col["name"] == name][0]
    results = collection["search"](name, bbox=bbox, time_range=time_range)
    return results