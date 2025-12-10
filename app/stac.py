import pystac_client
import planetary_computer
import json

def get_assets(collection):
    if collection == "landsat-c2-l2":
        return ["red", "green", "blue"]
    elif collection == "sentinel-2-l2a":
        return ["visual"]
    else:
        return ["visual"]

def search_microsoft(collection, bbox, time_range):
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )
    search = catalog.search(collections=[collection], bbox=bbox, datetime=time_range)
    items = search.item_collection()
    result = []
    
    for item in items:
        data = {
            "id": item.id,
            "date": item.properties["datetime"].split("T")[0],
            "time": item.properties["datetime"].split("T")[1].split(".")[0],
            "url": [a.href for a in item.assets.values() if a.media_type == "image/png"][0],
            "geometry": item.geometry,
            "bbox": item.bbox,
            "assets": json.dumps(get_assets(collection)),
            "stac_item": item.self_href
        }
        result.append(data)
    return result

def search_sentinel(bbox, time_range):
    results = search_microsoft("sentinel-2-l2a", bbox, time_range)
    return results