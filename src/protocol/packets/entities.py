from ...io.types import Bool, Bytes, OneOfMapped, String
from ...types.accounts import OfflineAccount
from ...types.entities import Player
from ..generic import GamePacket


class PlayerPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.entities.PlayerPacket"

    account: OneOfMapped(String, {"offline": OfflineAccount})
    player: Player
    just_joined: Bool


class PlayerPositionPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.PlayerPositionPacket"
    )


class EntityPositionPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.EntityPositionPacket"
    )


class NoClipPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.entities.NoClipPacket"


class SpawnEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.SpawnEntityPacket"
    )


class DespawnEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.DespawnEntityPacket"
    )


class AttackEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.AttackEntityPacket"
    )


class InteractEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.InteractEntityPacket"
    )


class HitEntityPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.entities.HitEntityPacket"


class MaxHPEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.MaxHPEntityPacket"
    )


class RespawnPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.entities.RespawnPacket"


class PlayerSkinPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.entities.PlayerSkinPacket"
    )

    player_unique_id: String
    skin: Bytes
