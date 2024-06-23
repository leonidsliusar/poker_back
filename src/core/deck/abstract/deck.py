from abc import ABC
from math import floor
from random import random

from src.core.cards.abstract.card import AbstractCard
from src.core.cards.card import Card
from src.core.cards.card_enum import SuitEnum, HigherRankEnum


class AbstractDeck(ABC):
    size: int
    cards: list[AbstractCard]

    def __init__(self):
        self.cards = []
        for rank in range(self.start_rank(), HigherRankEnum.highest() + 1):
            for suit in SuitEnum.enum_set():
                self.cards.append(Card(rank=rank, suit=getattr(SuitEnum, suit)))

    @classmethod
    def start_rank(cls) -> int:
        return HigherRankEnum.lowest() - cls.size // SuitEnum.length() + HigherRankEnum.length()

    def shuffle(self):
        """Fisher-Yates Shuffle
        https://gist.github.com/JenkinsDev/1e4bff898c72ec55df6f"""
        count = len(self.cards)
        while count > 1:
            i = int(floor(random() * count))
            count -= 1
            self.cards[i], self.cards[count] = self.cards[count], self.cards[i]

    @property
    def card(self) -> AbstractCard:
        return self.cards.pop()

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return str(self)