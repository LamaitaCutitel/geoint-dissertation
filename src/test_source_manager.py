from src.data_sources.source_manager import SourceManager
from config.settings import BBOX_GALATI


manager = SourceManager()

results = manager.search_all_sources(
    bbox=BBOX_GALATI,
    start_date="2024-01-01",
    end_date="2024-12-31",
    max_cloud=20,
    limit=20
)

print("\n=== CATALOG MULTI-SOURCE ===")
print("Total rezultate:", len(results))

for item in results[:10]:
    print(item["source"], "|", item["id"], "| cloud:", item["cloud_cover"], "|", item["datetime"])

manager.save_catalog(
    results,
    "data/output/geoint_multisource_catalog.json"
)