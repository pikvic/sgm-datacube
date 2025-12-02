import pystac_client
import planetary_computer


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
        }
        result.append(data)
    return result

def search_sentinel(bbox, time_range):
    results = search_microsoft("sentinel-2-l2a", bbox, time_range)
    return results