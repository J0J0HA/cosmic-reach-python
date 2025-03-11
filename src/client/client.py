import threading
from collections import defaultdict
from typing import Callable

from ..common.types import RememberedPlayer
from ..protocol import GamePacketRegistry, packets
from ..types.accounts import Account
from .base import BaseClient


class Client(BaseClient):
    """A client implementing basic functionality,
    like reading chat messages
    """
    
    VERSION = "0.4.1"
    "The version the client is made for"
    account: Account = None
    "The account the client is or will be logged in with"
    connected: bool = False
    "Whether the connection to the server was successfull"
    logged_in: bool = False
    "Whether the client has logged in yet"

    def __init__(self, account: Account):
        super().__init__()

        self.account = account
        self.players: dict[str, RememberedPlayer] = defaultdict(RememberedPlayer)

        self.add_event_handler(
            "packet", self._handle_protocol_sync, packets.meta.ProtocolSyncPacket
        )
        self.add_event_handler(
            "packet", self._handle_player_packet, packets.entities.PlayerPacket
        )
        self.add_event_handler(
            "packet", self._handle_player_skin_packet, packets.entities.PlayerSkinPacket
        )
        self.add_event_handler(
            "packet",
            lambda p: self._event_call(
                "chat", p.player_unique_id, (p.player_unique_id, p.message)
            ),
            packets.general.MessagePacket,
        )
        self.add_event_handler("connect", self._handle_login)

    def _handle_login(self):
        self.send_packet(packets.meta.LoginPacket(self.account))
        self.logged_in = True
        self._event_call("login")

    def _handle_player_packet(self, packet: packets.entities.PlayerPacket):
        if packet.account.unique_id not in self.players:
            self.players[packet.account.unique_id] = RememberedPlayer(
                packet.account, packet.player, skin=None
            )
        if packet.just_joined:
            self._event_call("join", packet.account.unique_id, (self.players[packet.account.unique_id],))
            
    def _handle_player_skin_packet(self, packet: packets.entities.PlayerSkinPacket):
        self.players[packet.player_unique_id].skin = packet.skin

    def _handle_protocol_sync(self, packet: packets.meta.ProtocolSyncPacket):
        if self.VERSION != packet.game_version:
            raise ValueError("[Protocol Sync] Game version mismatch")

        new_packets = GamePacketRegistry()

        for packet_name, packet_id in packet.packets:
            if packet_name not in self.packet_registry._packet_ids:
                raise ValueError(f"[Protocol Sync] Unknown packet: {packet_name}")

            if (packet_id == 1) ^ (
                packet_name
                == "finalforeach.cosmicreach.networking.packets.meta.ProtocolSyncPacket"
            ):
                raise ValueError(
                    "[Protocol Sync] Packet with id 1 must be ProtocolSyncPacket"
                )

            new_packets.register(
                self.packet_registry.get_packet_by_id(
                    self.packet_registry._packet_ids[packet_name]
                ),
                packet_id,
            )

        self.packet_registry = new_packets

        self.send_packet(
            packets.meta.ProtocolSyncPacket.create(self.packet_registry, self.VERSION)
        )
        self.connected = True
        self._event_call("connect")

    def _start_threaded(self, function: Callable):
        threading.Thread(target=function).start()
        
    def get_player(self, unique_id: str):
        """Get a player by his :code:``uniqueId``
        
        :raises KeyError: If the player is not known to the client
        """
        player = self.players[unique_id]
        if not player.is_known():
            raise KeyError(f"Player with uniqueId {unique_id} is unknown")
        return player

    def send_chat(self, message: str, display_name_prefix: bool = True):
        """Send a chat message
        
        :param message: The message to send
        :param display_name_prefix: Whether to prefix the display name
        """
        self.send_packet(
            packets.general.MessagePacket(
                (
                    (self.account.get_display_name() + "> ")
                    if display_name_prefix
                    else ""
                )
                + message,
                "",
            )
        )
