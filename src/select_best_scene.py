import json


def select_best_scene(json_path, max_cloud):
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    if not items:
        print("Nu exista rezultate.")
        return None

    # Filtrare după cloud cover
    filtered_items = [
        item for item in items
        if item["properties"].get("cloud_cover", 1) <= max_cloud
    ]

    if not filtered_items:
        print(f"Nu exista scene sub pragul de cloud cover: {max_cloud}")
        return None

    # Sortează după cloud cover crescător
    sorted_items = sorted(
        filtered_items,
        key=lambda x: x["properties"].get("cloud_cover", 1)
    )

    best = sorted_items[0]

    print("\nCea mai buna scena:")
    print("ID:", best["id"])
    print("Data:", best["properties"].get("acquired"))
    print("Cloud cover:", best["properties"].get("cloud_cover"))

    return best


if __name__ == "__main__":
    print("=== Selectare scenă optimă Planet ===")

    # Fișier JSON
    json_path = input(
        "Introdu calea fisierului JSON [default: data/output/planet_galati_items.json]: "
    ).strip()

    if not json_path:
        json_path = "data/output/planet_galati_items.json"

    # Prag cloud cover
    cloud_input = input(
        "Introdu pragul maxim cloud cover (ex: 0.2 pentru 20%) [default: 0.6]: "
    ).strip()

    if not cloud_input:
        max_cloud = 0.6
    else:
        try:
            max_cloud = float(cloud_input)
        except ValueError:
            print("Valoare invalida. Se foloseste default 0.6")
            max_cloud = 0.6

    select_best_scene(
        json_path=json_path,
        max_cloud=max_cloud
    )