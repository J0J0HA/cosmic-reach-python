import enum
from dataclasses import dataclass

from dataclasses_json import LetterCase, config

from ..io.types import JSONDataclass
from .java import Vec3


class PlayerGamemode(enum.Enum):
    SURVIVAL = "survival"
    CREATIVE = "creative"


@dataclass
class UniqueID(JSONDataclass):
    time: int
    rand: int
    number: int


@dataclass
class LocalBoundingBox(JSONDataclass):
    min: Vec3
    max: Vec3
    cnt: Vec3
    dim: Vec3


@dataclass
class Entity(JSONDataclass):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    unique_id: UniqueID
    position: Vec3
    last_position: Vec3
    view_position_offset: Vec3
    local_bounding_box: dict
    acceleration: Vec3 | None = None
    age: float | None = None


@dataclass
class SlotContainer(JSONDataclass):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    slots: str
    number_of_slots: int


@dataclass
class Player(JSONDataclass):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    gamemode: PlayerGamemode
    zone_id: str
    is_prone: bool
    entity: Entity
    inventory: SlotContainer
