from pathlib import Path
from src.common.types import RememberedPlayer
from src.client import Client
from src.protocol import packets
from src.types.accounts import OfflineAccount


def main():
    client = Client(OfflineAccount.with_name("Bot"))

    @client.on("login")
    def on_logged_in():
        client.send_chat("Hi, I just joined!")

    @client.on("chat")
    def on_chat(player_unique_id: str, message: str):
        player = client.get_player(player_unique_id)
        client.send_chat(f"{player.account.get_display_name()}? {message}, too!")
        if player.has_skin():
            Path("skin.png").write_bytes(player.skin)

    @client.on("join")
    def on_join(player: RememberedPlayer):
        client.send_chat(f"Hello {player.account.get_display_name()}!")

    client.connect("localhost", 47137)
    client.receive_packets()


if __name__ == "__main__":
    main()
