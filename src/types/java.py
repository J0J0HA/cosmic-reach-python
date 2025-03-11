from dataclasses import dataclass

from ..io.types import JSONDataclass


@dataclass
class Vec3(JSONDataclass):
    x: float = 0
    y: float = 0
    z: float = 0
