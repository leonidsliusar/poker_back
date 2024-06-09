from abc import ABC, abstractmethod

from core.cards.abstract.card import AbstractCard
from core.deck.abstract.deck import AbstractDeck
from core.player.abstract.player import AbstractPlayer


class AbstractRule(ABC):
    init_card_quantity: int | None = None

    def __init__(self, deck: AbstractDeck):
        self.deck = deck

    @property
    @abstractmethod
    def turn_of_player(self) -> tuple[AbstractPlayer, AbstractCard]:
        raise NotImplemented

    @turn_of_player.setter
    @abstractmethod
    def turn_of_player(self, data: tuple[AbstractPlayer, AbstractCard]):
        raise NotImplemented

    @abstractmethod
    def setup(self, players: list[AbstractPlayer]):
        raise NotImplemented
