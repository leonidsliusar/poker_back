from __future__ import annotations
from abc import ABC

from core.cards.card_enum import SuitEnum, HigherRankEnum


class AbstractCard(ABC):
    suit: SuitEnum
    rank: int

    def __init__(self, suit: SuitEnum, rank: int):
        self.suit = suit
        self.rank = rank

    def __le__(self, other: AbstractCard):
        return self.rank <= other.rank

    def __lt__(self, other: AbstractCard):
        return self.rank < other.rank

    def __ge__(self, other: AbstractCard):
        return self.rank >= other.rank

    def __gt__(self, other: AbstractCard):
        return self.rank > other.rank

    def __eq__(self, other: AbstractCard):
        return self.rank == other.rank and self.suit == other.suit

    def __str__(self) -> str:
        return f"{HigherRankEnum.name_by_value(self.rank)}{self.suit.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def same_suit(self, other: AbstractCard) -> bool:
        return self.suit == other.suit
