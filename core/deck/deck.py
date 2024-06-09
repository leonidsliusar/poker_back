from core.deck.abstract.deck import AbstractDeck


class ShortDeck(AbstractDeck):
    size: int = 36


class LongDeck(AbstractDeck):
    size: int = 52
