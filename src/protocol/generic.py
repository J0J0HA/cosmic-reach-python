import io
from typing import Optional

from ..io.types import IOType, bytes_to_buffer


class GamePacketRegistry:
    _packets: dict[int, type] = {}
    _packet_ids: dict[str, int] = {}

    def register(
        self,
        packet: "GamePacket",
        packet_id: Optional[int] = None,
    ):
        packet_id = packet_id or (len(self._packets) + 1)
        self._packets[packet_id] = packet
        self._packet_ids[packet.PACKET_NAME] = packet_id

    def get_packet_by_id(self, packet_id: int) -> "GamePacket":
        return self._packets[packet_id]

    def get_id_by_packet(self, packet: "GamePacket") -> int:
        return self._packet_ids[packet.PACKET_NAME]

    def serialize_cr_packet(self, packet: "GamePacket") -> bytes:
        return self.get_id_by_packet(packet).to_bytes(2, "big") + packet.to_cr_bytes()

    def deserialize_cr_packet(self, buf: io.BytesIO) -> bytes:
        packet_id = int.from_bytes(buf.read(2), "big")
        packet_class = self.get_packet_by_id(packet_id)
        return packet_class.from_cr_buffer(buf)

    def serialize_packet(self, packet: "GamePacket") -> bytes:
        packet = self.serialize_cr_packet(packet)
        return len(packet).to_bytes(4, "big") + packet

    def deserialize_packet(self, buf: io.BytesIO) -> bytes:
        length = int.from_bytes(buf.read(4), "big")
        buffer = io.BytesIO(buf.read(length))
        packet = self.deserialize_cr_packet(buffer)
        if leftovers := buffer.read():
            raise ValueError("Packet was not fully consumed. Leftovers:", leftovers)
        return packet


class GamePacket:
    __annotations__: dict[str, IOType]
    PACKET_NAME: str

    def __init__(self, *args):
        if len(args) != len(self.__annotations__):
            raise ValueError("Argument Amount Mismatch")

        for arg, (var, typ) in zip(args, self.__annotations__.items()):
            setattr(self, var, typ(arg) if not isinstance(arg, typ) else arg)

    def to_cr_bytes(self) -> bytes:
        return b"".join(
            typ.to_cr_bytes(getattr(self, var))
            for var, typ in self.__annotations__.items()
        )

    def to_cr_buffer(self, buf: io.BytesIO) -> None:
        return buf.write(self.to_cr_bytes())

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO):
        return cls(*(typ.from_cr_buffer(buf) for typ in cls.__annotations__.values()))

    @classmethod
    def from_cr_bytes(cls, _b: bytes) -> "IOType":
        return cls.from_cr_buffer(bytes_to_buffer(_b))

    def __repr__(self) -> str:
        return f"<{self.PACKET_NAME} {" ".join(key + "=" + repr(getattr(self, key)) for key in self.__annotations__)}>"
