from abc import ABC

from src.core.cards.abstract.card import AbstractCard


class AbstractPlayer(ABC):
    _address: str
    _hand: list[AbstractCard | None]
    _name: str | None
    _idx: int | None

    def __init__(self, address: str):
        self._address = address
        self._hand = []

    @property
    def idx(self) -> int:
        return self._idx

    @idx.setter
    def idx(self, idx: int):
        self._idx = idx

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def address(self) -> str:
        return self._address

    @property
    def hand(self) -> list[AbstractCard | None]:
        return self._hand

    def take_card(self, card: AbstractCard):
        self._hand.append(card)

    def turn(self, card: AbstractCard) -> AbstractCard:
        idx = self._hand.index(card)
        return self._hand.pop(idx)

    def drop_cards(self):
        self._hand.clear()
