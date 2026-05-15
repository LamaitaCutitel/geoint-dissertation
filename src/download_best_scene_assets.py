import json
import os
import requests

from config.settings import DATA_RAW


ASSETS_TO_DOWNLOAD = ["B03", "B08", "B11", "visual"]


def download_file(url, output_path):
    print(f"Download: {output_path}")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    print("Salvat:", output_path)


def download_best_scene_assets(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]
    asset_hrefs = scene.get("asset_hrefs", {})

    output_dir = os.path.join(DATA_RAW, scene_id)
    os.makedirs(output_dir, exist_ok=True)

    print("=== DOWNLOAD ASSET-URI SCENA ===")
    print("Scene ID:", scene_id)

    for asset_name in ASSETS_TO_DOWNLOAD:
        if asset_name not in asset_hrefs:
            print(f"Asset lipsa: {asset_name}")
            continue

        url = asset_hrefs[asset_name]

        if asset_name == "visual":
            filename = f"{scene_id}_{asset_name}.tif"
        else:
            filename = f"{scene_id}_{asset_name}.tif"

        output_path = os.path.join(output_dir, filename)

        download_file(url, output_path)


if __name__ == "__main__":
    download_best_scene_assets(
        "data/output/best_multisource_scene.json"
    )
