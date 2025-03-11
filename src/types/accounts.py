import random
from abc import ABC, abstractmethod

from ..io.types import JSONSerializable


class Account(JSONSerializable, ABC):
    account_type: str
    username: str
    unique_id: str

    def __init__(self, username: str, unique_id: str):
        self.username = username
        self.unique_id = unique_id

    def set_username(self, username: str):
        self.username = self.account_type + ":" + username

    def set_unique_id(self, unique_id):
        self.unique_id = self.account_type + ":" + str(unique_id)

    @abstractmethod
    def get_display_name(self) -> str: ...

    def get_dict(self) -> dict:
        return {"username": self.username, "uniqueId": self.unique_id}

    @classmethod
    def from_dict[T: "Account"](cls, data: dict) -> T:
        account = cls(data["username"], data["uniqueId"])
        return account

    def __str__(self) -> str:
        return f"{self.get_display_name()} ({self.unique_id})"


class OfflineAccount(Account):
    account_type = "offline"
    _display_name = "Player"

    def __init__(self, username: str, unique_id: str = None):
        if isinstance(username, OfflineAccount):
            super().__init__(username.username, username.unique_id)
            self.set_display_name(username.get_display_name())
            return
        if unique_id is None:
            unique_id = random.randint(0, 2147483647 + 1)
        super().__init__(username, unique_id)

    @classmethod
    def with_name(cls, name: str):
        acc = cls(f"offline:{name}")
        acc.set_display_name(name)
        return acc

    def get_dict(self) -> dict:
        return {"username": self.username, "uniqueId": self.unique_id}

    @classmethod
    def from_dict[T: "Account"](cls, data: dict) -> T:
        account = cls(data["username"], data["uniqueId"])
        return account

    def get_display_name(self):
        return self._display_name

    def set_display_name(self, name: str | None):
        if name is None:
            name = "Player"

        self._display_name = name
        self.set_username(name)
