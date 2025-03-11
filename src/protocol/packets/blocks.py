from ..generic import GamePacket


class PlaceBlockPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.blocks.PlaceBlockPacket"


class BreakBlockPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.blocks.BreakBlockPacket"


class InteractBlockPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.blocks.InteractBlockPacket"
    )


class BlockReplacePacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.blocks.BlockReplacePacket"
    )
