from collections import deque
from abc import ABC
from typing import TypeVar
from src.core.games.abstract.rule import AbstractRule
from src.core.player.abstract.player import AbstractPlayer


Players = TypeVar(name="Players", bound=[list[AbstractPlayer | None], deque[AbstractPlayer | None]])


class AbstractState(ABC):
    _players: Players
    rule: AbstractRule

    def __init__(self, rule: AbstractRule):
        self.rule = rule
        self._players = []

    def add_player(self, player: AbstractPlayer):
        player.idx = len(self._players)
        self._players.append(player)
        player.name = f"Player {len(self._players)}"

    @property
    def players(self):
        return self._players

    # @property
    # @abstractmethod
    # def next_player(self) -> AbstractPlayer:
    #     raise NotImplemented

    def start(self):
        self.rule.setup(self.players)
