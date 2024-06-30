from src.core.cards.card import Card
from src.core.cards.card_enum import SuitEnum


def test_card():
    card_1 = Card(rank=2, suit=SuitEnum.D)
    card_2 = Card(rank=2, suit=SuitEnum.D)
    card_3 = Card(rank=5, suit=SuitEnum.D)
    card_4 = Card(rank=10, suit=SuitEnum.C)
    assert card_1 == card_2
    assert card_1 is not card_2
    assert card_1 <= card_2 < card_3 < card_4
