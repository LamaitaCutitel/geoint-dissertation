from src.data_sources.planetary_computer_source import PlanetaryComputerSource
from config.settings import BBOX_GALATI


source = PlanetaryComputerSource()

results = source.search_sentinel2(
    bbox=BBOX_GALATI,
    start_date="2024-01-01",
    end_date="2024-12-31",
    max_cloud=60,
    limit=10
)

print("Numar rezultate:", len(results))

for item in results:
    print(item["id"], "| cloud:", item["cloud_cover"], "| date:", item["datetime"])
    print("Assets:", item["assets"])
    print("-" * 80)

source.save_results(
    results,
    "data/output/planetary_computer_sentinel2_galati.json"
)