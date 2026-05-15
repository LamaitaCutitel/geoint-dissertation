import json

from src.data_sources.planetary_computer_source import PlanetaryComputerSource


class SourceManager:
    def __init__(self):
        self.planetary_computer = PlanetaryComputerSource()

    def search_all_sources(self, bbox, start_date, end_date, max_cloud=60, limit=10):
        all_results = []

        print("Cautare in Microsoft Planetary Computer...")

        pc_results = self.planetary_computer.search_sentinel2(
            bbox=bbox,
            start_date=start_date,
            end_date=end_date,
            max_cloud=max_cloud,
            limit=limit
        )

        all_results.extend(pc_results)

        print(f"Rezultate Microsoft Planetary Computer: {len(pc_results)}")

        sorted_results = sorted(
            all_results,
            key=lambda item: item.get("cloud_cover", 100)
        )

        return sorted_results

    def save_catalog(self, results, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        print(f"Catalog multi-source salvat in: {output_path}")