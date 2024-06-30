import pytest

from src.core.cards.card import Card
from src.core.cards.card_enum import SuitEnum
from src.core.exceptions.exceptions import ComboError


def test_combo_error():
    card_1 = Card(rank=2, suit=SuitEnum.D)
    card_2 = Card(rank=2, suit=SuitEnum.D)
    card_3 = Card(rank=5, suit=SuitEnum.D)
    card_4 = Card(rank=10, suit=SuitEnum.C)
    with pytest.raises(ComboError) as exp:
        raise ComboError(combo=[card_1, card_2, card_3, card_4])
    assert str(exp.value) == f"ComboError {[card_1, card_2, card_3, card_4]}"
