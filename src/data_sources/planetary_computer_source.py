import json

import planetary_computer
from pystac_client import Client


class PlanetaryComputerSource:
    def __init__(self):
        self.catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
        self.catalog = Client.open(self.catalog_url)

    def search_sentinel2(self, bbox, start_date, end_date, max_cloud=60, limit=10):
        search = self.catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=f"{start_date}/{end_date}",
            query={
                "eo:cloud_cover": {
                    "lt": max_cloud
                }
            },
            limit=limit
        )

        items = list(search.items())
        results = []

        for item in items:
            signed_item = planetary_computer.sign(item)

            asset_names = list(signed_item.assets.keys())

            asset_hrefs = {}
            for asset_name, asset in signed_item.assets.items():
                asset_hrefs[asset_name] = asset.href

            results.append({
                "source": "Microsoft Planetary Computer",
                "collection": item.collection_id,
                "id": item.id,
                "datetime": item.datetime.isoformat() if item.datetime else None,
                "cloud_cover": item.properties.get("eo:cloud_cover"),
                "bbox": item.bbox,
                "assets": asset_names,
                "asset_hrefs": asset_hrefs
            })

        return results

    def save_results(self, results, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print(f"Rezultate salvate in: {output_path}")