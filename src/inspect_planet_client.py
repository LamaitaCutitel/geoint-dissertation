import asyncio
from planet import Auth, Session
from config.settings import PL_API_KEY


async def inspect_client():
    auth = Auth.from_key(PL_API_KEY)

    async with Session(auth=auth) as sess:
        client = sess.client("data")

        print("=== METODE DISPONIBILE DATA CLIENT ===")
        for name in dir(client):
            if "asset" in name.lower() or "item" in name.lower():
                print(name)


if __name__ == "__main__":
    asyncio.run(inspect_client())