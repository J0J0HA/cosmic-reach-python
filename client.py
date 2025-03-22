import asyncio
import os
from pathlib import Path

import dotenv

from cosmic_reach.client import Client
from cosmic_reach.common.types import RememberedPlayer
from cosmic_reach.protocol import packets
from cosmic_reach.types.json.accounts import ItchAccount


async def main():
    dotenv.load_dotenv()

    client = Client(ItchAccount.from_api_key(os.getenv("ITCH_API_KEY")))

    @client.events.join
    async def on_self_join():
        await client.send_chat("Hi, I just joined!")

    @client.events.chat
    async def on_chat(player_unique_id: str, message: str):
        player = client.get_player(player_unique_id)
        await client.send_chat(f"{player.account.display_name}? {message}, too!")
        if player.has_skin():
            Path("skin.png").write_bytes(player.skin)

    @client.events.player_join
    async def on_join(player: RememberedPlayer):
        print(player.account.display_name, "joined!")
        await client.send_chat(f"Hello {player.account.display_name}!")

    await client.connect("localhost", 47137)
    client.start()


if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_forever()
