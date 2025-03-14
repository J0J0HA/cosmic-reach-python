from dataclasses import dataclass

from ..types.json.accounts import Account
from ..types.json.entities import Player


@dataclass
class RememberedPlayer:
    account: Account | None = None
    player: Player | None = None
    skin: bytes | None = None

    def is_known(self) -> bool:
        return self.account is not None and self.player is not None

    def has_skin(self) -> bool:
        return self.skin is not None
