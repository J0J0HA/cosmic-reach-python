import random

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, LetterCase, config

class Account(DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    account_type: str
    username: str
    unique_id: str
    display_name: str


@dataclass
class OfflineAccount(Account):
    account_type: str = field(init=False, default="offline")
    
    username: str = field(default="offline:localPlayer")
    unique_id: str = field(default_factory=f"offline_id:{random.randint(0, 2147483647 + 1)}")
    display_name: str = field(default="Player")

    @classmethod
    def with_name(cls, name: str):
        acc = cls(f"offline:{name}", f"offline_id:{random.randint(0, 2147483647 + 1)}", name)
        return acc
