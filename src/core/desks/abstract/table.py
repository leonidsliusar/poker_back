import uuid
from abc import ABC, abstractmethod


class AbstractTable(ABC):
    id_: uuid
    max_players: int
    players: list = []

    def __init__(self):
        self.id_ = uuid.uuid4()

    @property
    def count_players(self) -> int:
        return len(self.players)

    def add_player(self, address: str):
        if self.count_players < self.max_players:
            self.players.append(address)
        else:
            print("Create New Table")

    def remove_player(self, address: str):
        self.players.remove(address)
        