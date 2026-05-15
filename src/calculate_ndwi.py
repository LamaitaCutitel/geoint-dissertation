import json
import os

import numpy as np
import rasterio

from config.settings import DATA_RAW, DATA_PROCESSED


def calculate_ndwi(green_path, nir_path, output_path):
    with rasterio.open(green_path) as green_src:
        green = green_src.read(1).astype("float32")
        profile = green_src.profile

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype("float32")

    ndwi = (green - nir) / (green + nir + 1e-10)

    profile.update(
        dtype=rasterio.float32,
        count=1,
        compress="lzw"
    )

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(ndwi.astype(rasterio.float32), 1)

    print("NDWI salvat in:", output_path)


def run(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]

    scene_raw_dir = os.path.join(DATA_RAW, scene_id)
    scene_processed_dir = os.path.join(DATA_PROCESSED, scene_id)

    os.makedirs(scene_processed_dir, exist_ok=True)

    green_path = os.path.join(scene_raw_dir, f"{scene_id}_B03.tif")
    nir_path = os.path.join(scene_raw_dir, f"{scene_id}_B08.tif")

    output_path = os.path.join(scene_processed_dir, f"{scene_id}_NDWI.tif")

    calculate_ndwi(
        green_path=green_path,
        nir_path=nir_path,
        output_path=output_path
    )


if __name__ == "__main__":
    run("data/output/best_multisource_scene.json")