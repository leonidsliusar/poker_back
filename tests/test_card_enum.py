from src.core.cards.card_enum import SuitEnum, HigherRankEnum


def test_suit_enum():
    assert SuitEnum.enum_set() == ["D", "H", "C", "S"]
    assert SuitEnum.length() == 4


def test_higher_rank_enum():
    assert HigherRankEnum.highest() == 14
    assert HigherRankEnum.length() == 4
    assert HigherRankEnum.lowest() == 11
