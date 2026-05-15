import json
import os

import numpy as np
import rasterio

from config.settings import DATA_PROCESSED


def generate_water_mask(ndwi_path, output_path, threshold=0.2):
    with rasterio.open(ndwi_path) as src:
        ndwi = src.read(1)
        profile = src.profile

    water_mask = np.where(ndwi > threshold, 1, 0)

    profile.update(
        dtype=rasterio.uint8,
        count=1,
        compress="lzw"
    )

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(water_mask.astype(rasterio.uint8), 1)

    print("Water mask salvata in:", output_path)


def run(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]
    scene_processed_dir = os.path.join(DATA_PROCESSED, scene_id)

    ndwi_path = os.path.join(scene_processed_dir, f"{scene_id}_NDWI.tif")
    output_path = os.path.join(scene_processed_dir, f"{scene_id}_water_mask.tif")

    threshold_input = input("Introdu threshold NDWI [default: 0.2]: ").strip()

    if not threshold_input:
        threshold = 0.2
    else:
        threshold = float(threshold_input)

    generate_water_mask(
        ndwi_path=ndwi_path,
        output_path=output_path,
        threshold=threshold
    )


if __name__ == "__main__":
    run("data/output/best_multisource_scene.json")