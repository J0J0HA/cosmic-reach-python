import asyncio
from pathlib import Path
from src.common.types import RememberedPlayer
from src.client import Client
from src.protocol import packets
from src.types.json.accounts import OfflineAccount


async def main():
    client = Client(OfflineAccount.with_name("Bot"))

    @client.events.login
    async def on_logged_in():
        await client.send_chat("Hi, I just logged in!")

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
