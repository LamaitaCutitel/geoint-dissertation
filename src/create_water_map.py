import json
import os

import folium
import geopandas as gpd

from config.settings import DATA_OUTPUT


def create_map(water_vector_path, output_html):
    water = gpd.read_file(water_vector_path)
    water = water.to_crs(epsg=4326)

    center = water.geometry.union_all().centroid

    m = folium.Map(
        location=[center.y, center.x],
        zoom_start=11,
        tiles="OpenStreetMap"
    )

    folium.GeoJson(
        water,
        name="Zone apa / posibile inundatii",
        tooltip=folium.GeoJsonTooltip(
            fields=["area_m2"],
            aliases=["Suprafata m2:"]
        )
    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save(output_html)

    print("Harta HTML salvata in:", output_html)


def run(scene_path):
    with open(scene_path, "r", encoding="utf-8") as f:
        scene = json.load(f)

    scene_id = scene["id"]

    output_dir = os.path.join(DATA_OUTPUT, scene_id)

    water_vector_path = os.path.join(output_dir, f"{scene_id}_water_polygons.gpkg")
    output_html = os.path.join(output_dir, f"{scene_id}_water_map.html")

    create_map(water_vector_path, output_html)


if __name__ == "__main__":
    run("data/output/best_multisource_scene.json")