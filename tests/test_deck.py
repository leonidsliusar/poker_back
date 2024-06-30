import copy

import pytest

from src.core.cards.card import Card
from src.core.cards.card_enum import SuitEnum
from src.core.deck.deck import LongDeck, ShortDeck


@pytest.mark.parametrize("start_rank, deck_class", [(2, LongDeck), (6, ShortDeck)])
def test_deck_init(start_rank, deck_class):
    deck = deck_class()
    expected_cards = ([Card(rank=rank, suit=SuitEnum.D) for rank in range(start_rank, 15)]
                      + [Card(rank=rank, suit=SuitEnum.C) for rank in range(start_rank, 15)]
                      + [Card(rank=rank, suit=SuitEnum.S) for rank in range(start_rank, 15)]
                      + [Card(rank=rank, suit=SuitEnum.H) for rank in range(start_rank, 15)])
    for card in deck.cards:
        assert card in expected_cards


def test_start_rank():
    assert LongDeck.start_rank() == 2
    assert ShortDeck.start_rank() == 6


def test_shuffle():
    deck = LongDeck()
    init_deck = copy.copy(deck.cards)
    deck.shuffle()
    assert init_deck != deck.cards
