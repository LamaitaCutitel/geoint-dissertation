from datetime import datetime, timezone

from src.planet_insights_client import PlanetInsightsClient, run_async
from config.settings import BBOX_GALATI


def bbox_to_geojson_polygon(bbox):
    min_lon, min_lat, max_lon, max_lat = bbox

    return {
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat],
            [max_lon, min_lat],
            [max_lon, max_lat],
            [min_lon, max_lat],
            [min_lon, min_lat]
        ]]
    }


client = PlanetInsightsClient()

geometry = bbox_to_geojson_polygon(BBOX_GALATI)

items = run_async(
    client.search_planetscope_items(
        geometry=geometry,
        start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2024, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
        limit=100
    )
)

print("Numar rezultate Galați:", len(items))

for item in items:
    print(item["id"])

import json

with open("data/output/planet_galati_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=4)

print("Rezultatele au fost salvate în data/output/planet_galati_items.json")