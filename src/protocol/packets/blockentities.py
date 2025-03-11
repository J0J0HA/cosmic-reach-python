from ..generic import GamePacket


class BlockEntityDataPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.blockentities.BlockEntityDataPacket"


class BlockEntityScreenPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.blockentities.BlockEntityScreenPacket"


class SignsEntityPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.blockentities.SignsEntityPacket"
    )
