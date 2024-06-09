from core.cards.card import Card
from core.cards.card_enum import SuitEnum
from core.player.player import Player


def test_player():
    player = Player(address="test_address")
    player.name = "Player 1"
    assert player.name == "Player 1"
    assert player.hand == []
    card_1 = Card(rank=2, suit=SuitEnum.D)
    card_2 = Card(rank=5, suit=SuitEnum.D)
    card_3 = Card(rank=10, suit=SuitEnum.C)
    player.take_card(card_1)
    assert player.hand == [card_1]
    player.take_card(card_2)
    assert player.hand == [card_1, card_2]
    player.turn(card_2)
    player.take_card(card_3)
    assert player.hand == [card_1, card_3]
    player.drop_cards()
    assert player.hand == []
