from ..generic import GamePacket


class PlaySound2DPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.sounds.PlaySound2DPacket"


class PlaySound3DPacket(GamePacket):
    PACKET_NAME = "finalforeach.cosmicreach.networking.packets.sounds.PlaySound3DPacket"


class SetMusicTagsPacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.sounds.SetMusicTagsPacket"
    )


class ForceSongChangePacket(GamePacket):
    PACKET_NAME = (
        "finalforeach.cosmicreach.networking.packets.sounds.ForceSongChangePacket"
    )
