import json


REQUIRED_ASSETS = ["B03", "B08", "B11", "visual"]


def has_required_assets(item):
    assets = item.get("assets", [])
    return all(asset in assets for asset in REQUIRED_ASSETS)


def select_best_scene(catalog_path):
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    valid_items = [
        item for item in catalog
        if has_required_assets(item)
    ]

    if not valid_items:
        print("Nu exista scene cu asset-urile necesare.")
        return None

    sorted_items = sorted(
        valid_items,
        key=lambda item: item.get("cloud_cover", 100)
    )

    best = sorted_items[0]

    print("\n=== CEA MAI BUNA SCENA MULTI-SOURCE ===")
    print("Source:", best["source"])
    print("ID:", best["id"])
    print("Datetime:", best["datetime"])
    print("Cloud cover:", best["cloud_cover"])
    print("Assets utile:", REQUIRED_ASSETS)

    with open("data/output/best_multisource_scene.json", "w", encoding="utf-8") as f:
        json.dump(best, f, indent=4)

    print("\nScena selectata a fost salvata in:")
    print("data/output/best_multisource_scene.json")

    return best


if __name__ == "__main__":
    select_best_scene(
        "data/output/geoint_multisource_catalog.json"
    )
