import json
import os

import rasterio

from config.settings import DATA_RAW


ASSETS = ["B03", "B08", "B11", "visual"]


def inspect_raster(path):
    with rasterio.open(path) as src:
        print("\n=== RASTER INFO ===")
        print("Fisier:", path)
        print("CRS:", src.crs)
        print("Dimensiuni:", src.width, "x", src.height)
        print("Numar benzi:", src.count)
        print("Rezolutie:", src.res)
        print("Bounds:", src.bounds)
        print("Tip date:", src.dtypes)


def inspect_scene(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]
    scene_dir = os.path.join(DATA_RAW, scene_id)

    print("=== INSPECTARE RASTERE DESCARCATE ===")
    print("Scene ID:", scene_id)
    print("Folder:", scene_dir)

    for asset in ASSETS:
        raster_path = os.path.join(scene_dir, f"{scene_id}_{asset}.tif")

        if not os.path.exists(raster_path):
            print(f"\nLipseste fisierul pentru asset: {asset}")
            continue

        inspect_raster(raster_path)


if __name__ == "__main__":
    inspect_scene("data/output/best_multisource_scene.json")