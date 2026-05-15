import json
import asyncio

from planet import Auth, Session

from config.settings import PL_API_KEY


class PlanetAssetChecker:
    def __init__(self):
        self.auth = Auth.from_key(PL_API_KEY)

    async def check_assets(self, scene_id):
        async with Session(auth=self.auth) as sess:
            client = sess.client("data")

            item = await client.get_item(
                item_type_id="PSScene",
                item_id=scene_id
            )
            assets = item.get("_links", {})

            print("\n=== SCENE ASSETS ===")
            print("Scene ID:", scene_id)

            if not assets:
                print("Nu exista asset-uri disponibile.")
                return item

            for key, value in assets.items():
                print(f"{key}: {value}")

            return item


def run_async(coro):
    return asyncio.run(coro)


if __name__ == "__main__":
    print("=== Verificare asset-uri scenă Planet ===")

    with open("data/output/best_scene_details.json", "r", encoding="utf-8") as f:
        best_scene = json.load(f)

    scene_id = best_scene["id"]

    checker = PlanetAssetChecker()

    run_async(
        checker.check_assets(scene_id)
    )