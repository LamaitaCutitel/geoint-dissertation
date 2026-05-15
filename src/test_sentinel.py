from planet_insights_client import SentinelHubClient
from config.settings import BBOX_GALATI

client = SentinelHubClient()

print("Conectare Sentinel Hub...")

data = client.download_sentinel1(
    bbox_coords=BBOX_GALATI,
    time_interval=("2024-01-01", "2024-01-10")
)

print("Download finalizat.")
print("Numar imagini:", len(data))