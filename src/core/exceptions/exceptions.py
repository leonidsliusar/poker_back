from src.core.cards.abstract.card import AbstractCard


class ComboError(Exception):
    combo: list[AbstractCard]

    def __init__(self, combo: list[AbstractCard]):
        self.combo = combo

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.combo}"
