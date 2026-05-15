import json
import os

import geopandas as gpd
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape

from config.settings import DATA_PROCESSED, DATA_OUTPUT


def vectorize_mask(mask_path, output_path):
    with rasterio.open(mask_path) as src:
        mask = src.read(1)
        transform = src.transform
        crs = src.crs

        results = []

        for geom, value in shapes(mask, mask=mask == 1, transform=transform):
            if value == 1:
                results.append({
                    "geometry": shape(geom),
                    "value": int(value)
                })

    if not results:
        print("Nu au fost gasite poligoane de apa.")
        return

    gdf = gpd.GeoDataFrame(results, crs=crs)

    gdf["area_m2"] = gdf.to_crs(epsg=3857).area

    gdf.to_file(output_path)

    print("Poligoane apa salvate in:", output_path)
    print("Numar poligoane:", len(gdf))
    print("Suprafata totala estimata m2:", round(gdf["area_m2"].sum(), 2))
    print("Suprafata totala estimata km2:", round(gdf["area_m2"].sum() / 1_000_000, 4))


def run(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]

    scene_processed_dir = os.path.join(DATA_PROCESSED, scene_id)
    output_dir = os.path.join(DATA_OUTPUT, scene_id)

    os.makedirs(output_dir, exist_ok=True)

    mask_path = os.path.join(scene_processed_dir, f"{scene_id}_water_mask.tif")
    output_path = os.path.join(output_dir, f"{scene_id}_water_polygons.gpkg")

    vectorize_mask(mask_path, output_path)


if __name__ == "__main__":
    run("data/output/best_multisource_scene.json")