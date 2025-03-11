from ..generic import GamePacket


class DropItemPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.items.DropItemPacket"


class SlotInteractPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.items.SlotInteractPacket"


class ContainerSyncPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.items.ContainerSyncPacket"
    )


class RequestGiveItemPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.items.RequestGiveItemPacket"
    )


class SlotSyncPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.items.SlotSyncPacket"


class SlotSwapPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.items.SlotSwapPacket"


class SlotMergePacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.items.SlotMergePacket"
