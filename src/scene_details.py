import json


def load_best_scene(json_path, max_cloud):
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    filtered_items = [
        item for item in items
        if item["properties"].get("cloud_cover", 1) <= max_cloud
    ]

    if not filtered_items:
        print("Nu exista scene sub pragul selectat.")
        return None

    sorted_items = sorted(
        filtered_items,
        key=lambda x: x["properties"].get("cloud_cover", 1)
    )

    return sorted_items[0]


def print_scene_details(scene):
    print("\n=== DETALII SCENA ===")
    print("ID:", scene.get("id"))
    print("Tip:", scene.get("properties", {}).get("item_type"))
    print("Data achizitie:", scene.get("properties", {}).get("acquired"))
    print("Cloud cover:", scene.get("properties", {}).get("cloud_cover"))
    print("Rezolutie:", scene.get("properties", {}).get("gsd"))
    print("Instrument:", scene.get("properties", {}).get("instrument"))
    print("Satellite ID:", scene.get("properties", {}).get("satellite_id"))
    print("Publishing stage:", scene.get("properties", {}).get("publishing_stage"))


def save_scene_details(scene, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scene, f, indent=4)

    print(f"\nDetaliile au fost salvate in: {output_path}")


if __name__ == "__main__":
    print("=== Inspector scenă Planet ===")

    json_path = input(
        "Introdu fisierul JSON [default: data/output/planet_galati_items.json]: "
    ).strip()

    if not json_path:
        json_path = "data/output/planet_galati_items.json"

    cloud_input = input(
        "Introdu prag cloud cover [default: 0.6]: "
    ).strip()

    if not cloud_input:
        max_cloud = 0.6
    else:
        max_cloud = float(cloud_input)

    best_scene = load_best_scene(json_path, max_cloud)

    if best_scene:
        print_scene_details(best_scene)

        save_scene_details(
            best_scene,
            "data/output/best_scene_details.json"
        )