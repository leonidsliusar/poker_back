from abc import ABC, abstractmethod

from src.core.deck.abstract.deck import AbstractDeck
from src.core.player.abstract.player import AbstractPlayer


class AbstractRule(ABC):
    init_card_quantity: int | None = None

    def __init__(self, deck: AbstractDeck):
        self.deck = deck

    def reload_deck(self):
        reloaded_deck = self.deck.__init__()
        self.deck = reloaded_deck

    @abstractmethod
    def setup(self, players: list[AbstractPlayer], *args, **kwargs):
        raise NotImplemented
