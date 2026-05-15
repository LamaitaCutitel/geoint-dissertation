import asyncio
from planet import Auth, Session
from planet import data_filter

from config.settings import PL_API_KEY


class PlanetInsightsClient:
    def __init__(self):
        self.auth = Auth.from_key(PL_API_KEY)

    async def search_planetscope_items(self, geometry, start_date, end_date, limit=10):
        async with Session(auth=self.auth) as sess:
            client = sess.client("data")

            filters = data_filter.and_filter([
                data_filter.geometry_filter(geometry),
                data_filter.date_range_filter(
                    "acquired",
                    gte=start_date,
                    lte=end_date
                )
            ])

            results = []

            async for item in client.search(
                item_types=["PSScene"],
                search_filter=filters,
                limit=limit
            ):
                results.append(item)

            return results

            return results
    async def search_recent_planetscope_items(self, start_date, end_date, limit=5):
        async with Session(auth=self.auth) as sess:
            client = sess.client("data")

            filters = data_filter.and_filter([
                data_filter.date_range_filter(
                    "acquired",
                    gte=start_date,
                    lte=end_date
                )
            ])

            results = []

            async for item in client.search(
                item_types=["PSScene"],
                search_filter=filters,
                limit=limit
            ):
                results.append(item)

            return results 


def run_async(coro):
    return asyncio.run(coro)