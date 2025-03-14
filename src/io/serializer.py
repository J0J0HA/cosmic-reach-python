import io
from typing import Any, Callable
import typing


class Store:
    serializers: dict[type, Callable[[type, Any], bytes]]
    deserializers: dict[type, Callable[[type, io.BytesIO], Any]]
    
    def __init__(self):
        self.serializers = {}
        self.deserializers = {}

store = Store()


def serializer_for(cls) -> Callable[[Callable[[type, Any], bytes]], Callable[[type, Any], bytes]]:
    def decorator(func: Callable[[type, Any], bytes]):
        store.serializers[cls] = func
        return func

    return decorator


def deserializer_for(
    cls,
) -> Callable[[Callable[[type, io.BytesIO], Any]], Callable[[type, io.BytesIO], Any]]:
    def decorator(func: Callable[[type, io.BytesIO], Any]):
        store.deserializers[cls] = func
        return func

    return decorator


def serialize(obj: Any, typ: type | None = None) -> bytes:
    if typ is None:
        typ = type(obj)
    if typ == typing.Union:
        serializer = store.deserializers[typing.Union]
    else:
        comp = isinstance if not isinstance(typ, type) else issubclass
        for made_for, serializer in store.serializers.items():
            if made_for == typing.Union:
                continue
            if comp(typ, made_for):
                break
        else:
            raise TypeError(f"Objects of type {typ} cannot be serialized")
    try:
        return serializer(typ, obj)
    except Exception as e:
        e.add_note(f"CONTEXT>> While serializing object of type {typ}")
        raise e


def deserialize[T: Any](typ: type[T], buf: io.BytesIO) -> T:
    if typ == typing.Union:
        deserializer = store.deserializers[typing.Union]
    else:
        comp = isinstance if not isinstance(typ, type) else issubclass
        for made_for, deserializer in store.deserializers.items():
            if made_for == typing.Union:
                continue
            if comp(typ, made_for):
                break
        else:
            raise TypeError(f"Objects of type {typ} cannot be deserialized")
    try:
        return deserializer(typ, buf)
    except Exception as e:
        e.add_note(f"CONTEXT>> While deserializing object of type {typ}")
        raise e
