from ...io.types import JSON, Bool, Long, String
from ..generic import GamePacket


class EndTickPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.EndTickPacket"
    world_tick: Long


class MessagePacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.MessagePacket"
    message: String
    player_unique_id: String


class ZonePacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.ZonePacket"

    set_default: Bool
    zone: JSON


class ChunkColumnPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.ChunkColumnPacket"


class CommandPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.CommandPacket"


class ParticleSystemPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.ParticleSystemPacket"
