import io
import json
import struct
from abc import ABC, ABCMeta, abstractmethod
from typing import Any

from dataclasses_json import DataClassJsonMixin

from . import wjson


def bytes_to_buffer(_b: bytes):
    return io.BytesIO(_b)


def buffer_to_bytes(buf: io.BytesIO) -> bytes:
    return buf.read()


def consuming_unpack(format_: str, buf: io.BytesIO) -> tuple:
    return struct.unpack(format_, buf.read(struct.calcsize(format)))


class ABCIOTypeMeta(ABCMeta):
    def __or__(self, other: "IOType") -> "Union":
        return Union(Byte, (self, other))


class ABCIOType(metaclass=ABCIOTypeMeta):
    _FOR: type

    def to_cr_bytes(self) -> bytes:
        raise NotImplementedError

    def to_cr_buffer(self, buf: io.BytesIO) -> None:
        return buf.write(self.to_cr_bytes())

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "IOType":
        raise NotImplementedError

    @classmethod
    def from_cr_bytes(cls, _b: bytes) -> "IOType":
        return cls.from_cr_buffer(bytes_to_buffer(_b))


class IOTypeMeta(type):
    def __or__(self, other: "IOType") -> "Union":
        return Union(Byte, self, other)


class IOType(metaclass=IOTypeMeta):
    _FOR: type

    def to_cr_bytes(self) -> bytes:
        raise NotImplementedError

    def to_cr_buffer(self, buf: io.BytesIO) -> None:
        return buf.write(self.to_cr_bytes())

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "IOType":
        raise NotImplementedError

    @classmethod
    def from_cr_bytes(cls, _b: bytes) -> "IOType":
        return cls.from_cr_buffer(bytes_to_buffer(_b))


class Bool(int, IOType):
    _FOR = bool

    def to_cr_bytes(self) -> bytes:
        return int.to_bytes(1, "big")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> bool:
        return bool(cls.from_bytes(buf.read(1), "big"))


class Byte(int, IOType):
    _FOR = int

    def to_cr_bytes(self) -> bytes:
        return int.to_bytes(1, "big")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Byte":
        return cls(cls.from_bytes(buf.read(1), "big"))


class Int(int, IOType):
    _FOR = int

    def to_cr_bytes(self) -> bytes:
        return self.to_bytes(4, "big")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Int":
        return cls.from_bytes(buf.read(4), "big")


class Long(int, IOType):
    _FOR = int

    def to_cr_bytes(self) -> bytes:
        return self.to_bytes(8, "big")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Long":
        return cls.from_bytes(buf.read(8), "big")


class Float(float, IOType):
    _FOR = float

    def to_cr_bytes(self) -> bytes:
        return struct.pack(">f", self)

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Float":
        return cls(consuming_unpack(">f", buf)[0])


class Double(float, IOType):
    _FOR = int

    def to_cr_bytes(self) -> bytes:
        return struct.pack(">d", self)

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Double":
        return cls(consuming_unpack(">d", buf)[0])


class Short(int, IOType):
    _FOR = int

    def to_cr_bytes(self) -> bytes:
        return self.to_bytes(2, "big")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Short":
        return cls.from_bytes(buf.read(2), "big")


class Bytes(bytes, IOType):
    _FOR = str

    def to_cr_bytes(self) -> bytes:
        if len(self) == 0:
            return (-1).to_bytes(4, "big", signed=True)
        return len(self).to_bytes(4, "big") + self

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Short":
        length = int.from_bytes(buf.read(4), "big")
        if length == -1:
            return ""
        return cls(buf.read(length))


class String(str, IOType):
    _FOR = str

    def to_cr_bytes(self) -> bytes:
        if len(self) == 0:
            return (-1).to_bytes(4, "big", signed=True)
        return len(self).to_bytes(4, "big") + self.encode("utf-8")

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Short":
        length = int.from_bytes(buf.read(4), "big")
        if length == -1:
            return ""
        return cls(buf.read(length).decode("utf-8"))


class JSON(dict, IOType):
    _FOR = dict

    def to_cr_bytes(self) -> bytes:
        return String(json.dumps(self)).to_cr_bytes()

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> "Int":
        st = String.from_cr_buffer(buf)
        return cls(wjson.loads(st))


class IJSONSerializable(ABC):
    @abstractmethod
    def get_dict(self) -> dict: ...

    @classmethod
    @abstractmethod
    def from_dict[T: "IJSONSerializable"](cls: T, data: dict) -> T: ...


class JSONSerializable[T: IJSONSerializable](IJSONSerializable, ABCIOType):
    _FOR = IJSONSerializable

    def to_cr_bytes(self) -> bytes:
        return JSON(self.get_dict()).to_cr_bytes()

    @classmethod
    def from_cr_buffer(cls, buf: io.BytesIO) -> T:
        return cls.from_dict(JSON.from_cr_buffer(buf))


class JSONDataclass(DataClassJsonMixin):
    _FOR = DataClassJsonMixin

    def to_cr_bytes(self) -> bytes:
        return JSON(self.schema().dump(self)).to_cr_bytes()

    @classmethod
    def from_cr_buffer[T: "JSONDataclass"](cls: T, buf: io.BytesIO) -> T:
        return cls.schema().load(JSON.from_cr_buffer(buf))


def Tuple(*typs: type[IOType]) -> type[IOType]:
    class _Tuple(tuple[typs], IOType):
        _FOR = tuple

        def to_cr_bytes(self) -> bytes:
            return b"".join(typ.to_cr_bytes(item) for typ, item in zip(typs, self))

        @classmethod
        def from_cr_buffer(cls, buf: io.BytesIO) -> "Int":
            return cls(typ.from_cr_buffer(buf) for typ in typs)

    return _Tuple


def Repeat[T: IOType](typ: type[T], amount: type[IOType]) -> type[IOType]:
    class _Repeat(list[T], IOType):
        _FOR = list

        def to_cr_bytes(self) -> bytes:
            return bytes(
                amount.to_cr_bytes(len(self))
                + b"".join(typ.to_cr_bytes(item) for item in self)
            )

        @classmethod
        def from_cr_buffer(cls, buf: io.BytesIO) -> "Int":
            length = amount.from_cr_buffer(buf)
            return cls(typ.from_cr_buffer(buf) for _ in range(length))

    return _Repeat


def Union[T: IOType](declare_typ: type[IOType], *typs: T) -> T:
    class _UnionMeta(IOTypeMeta):
        def __call__(self, value: T):
            if not any(isinstance(value, typ._FOR) for typ in typs):
                raise TypeError("Union does not support that type")
            return value

        def __or__(self, other: IOType):
            return Union(declare_typ, *typs, other)

    class _Union(IOType, metaclass=_UnionMeta):
        def to_cr_bytes(self) -> bytes:
            for idx, typ in enumerate(typs):
                if isinstance(self, typ._FOR):
                    return declare_typ.to_cr_bytes(idx) + typ(self).to_cr_bytes()
            raise TypeError("Union does not support that type")

        @classmethod
        def from_cr_buffer(cls, buf: io.BytesIO) -> T:
            typ_idx = declare_typ.from_cr_buffer(buf)
            return typs[typ_idx].from_cr_buffer(buf)

    return _Union


def OneOfMapped[T: IOType](declare_typ: type[IOType], typs: dict[Any, T]) -> T:
    class _OneOfMappedMeta(IOTypeMeta):
        def __call__(self, value: T):
            if not any(isinstance(value, typ._FOR) for typ in typs.values()):
                raise TypeError("OneOfMapped does not support that type")
            return value

    class _OneOfMapped(IOType, metaclass=_OneOfMappedMeta):
        def to_cr_bytes(self) -> bytes:
            for mdx, typ in typs.items():
                if isinstance(self, typ._FOR):
                    return declare_typ.to_cr_bytes(mdx) + typ(self).to_cr_bytes()
            raise TypeError("OneOfMapped does not support that type")

        @classmethod
        def from_cr_buffer(cls, buf: io.BytesIO) -> T:
            typ_mdx = declare_typ.from_cr_buffer(buf)
            return typs[typ_mdx].from_cr_buffer(buf)

    return _OneOfMapped
