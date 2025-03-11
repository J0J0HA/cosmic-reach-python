from ...io.types import (
    Bool,
    Int,
    Long,
    OneOfMapped,
    Repeat,
    String,
    Tuple,
)
from ...types.accounts import OfflineAccount
from ..generic import GamePacket, GamePacketRegistry


class ProtocolSyncPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.ProtocolSyncPacket"
    packets: Repeat(Tuple(String, Int), Int)
    game_version: String

    @classmethod
    def create(cls, packet_registry: GamePacketRegistry, game_version: str):
        return cls(
            [
                (packet.PACKET_NAME, packet_id)
                for packet_id, packet in packet_registry._packets.items()
            ],
            game_version,
        )


class TransactionPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.TransactionPacket"
    id: Long


class LoginPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.LoginPacket"
    account: OneOfMapped(String, {"offline": OfflineAccount})


class RemovedPlayerPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.RemovedPlayerPacket"
    account_id: String


class WorldRecievedGamePacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.meta.WorldRecievedGamePacket"
    )


class SetNetworkSetting(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.SetNetworkSetting"
    key: String
    value: Bool | Int


class ChallengeLoginPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.meta.ChallengeLoginPacket"
    )
    challenge: String


class ItchSessionTokenPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.meta.ItchSessionTokenPacket"
    )
    session_token: String


class DisconnectPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.meta.DisconnectPacket"
    reason: String
