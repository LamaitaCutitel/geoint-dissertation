import json
import asyncio

from planet import Auth, Session

from config.settings import PL_API_KEY


class PlanetAssetChecker:
    def __init__(self):
        self.auth = Auth.from_key(PL_API_KEY)

    async def find_scene_with_assets(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            scenes = json.load(f)

        async with Session(auth=self.auth) as sess:
            client = sess.client("data")

            for scene in scenes:
                scene_id = scene["id"]

                assets = await client.list_item_assets(
                    item_type_id="PSScene",
                    item_id=scene_id
                )

                print("\nScene ID:", scene_id)

                if not assets:
                    print("Fara asset-uri disponibile.")
                    continue

                print("Asset-uri gasite:")

                for asset_name, asset_data in assets.items():
                    print("-", asset_name, "| status:", asset_data.get("status"))

                with open("data/output/scene_with_assets.json", "w", encoding="utf-8") as f:
                    json.dump(scene, f, indent=4)

                print("\nScena salvata in data/output/scene_with_assets.json")
                return scene

            print("\nNu a fost gasita nicio scena cu asset-uri disponibile.")
            return None


def run_async(coro):
    return asyncio.run(coro)


if __name__ == "__main__":
    checker = PlanetAssetChecker()

    run_async(
        checker.find_scene_with_assets(
            "data/output/planet_galati_items.json"
        )
    )