import pytest

from src.core.cards.card import Card
from src.core.cards.card_enum import SuitEnum
from src.core.deck.deck import ShortDeck
from src.core.games.durak.rule import DurakRule
from src.core.games.texas_holdem.rule import HoldEmPokerRule
from src.core.player.player import Player


def test_durak_rule():
    deck = ShortDeck()
    rule = DurakRule(deck)
    player_1 = Player(address="test_1")
    player_2 = Player(address="test_2")
    players = [player_1, player_2]
    rule.setup(players)
    assert rule.trump
    turn_of_player = rule.turn_of_player[0]
    assert turn_of_player
    defender = player_2 if turn_of_player is player_1 else player_1
    attacker = player_2 if defender is player_1 else player_1
    attack_card = rule.attack(card=turn_of_player.hand[0], next_player=defender)
    turn_of_player = rule.turn_of_player[0]
    rule.defend(card=turn_of_player.hand[0], next_player=attacker)


@pytest.mark.parametrize("attack_rank, defend_rank", [(10, 11), (12, 11)])
def test_durak_rule_attack(attack_rank, defend_rank):
    deck = ShortDeck()
    rule = DurakRule(deck)
    attacker = Player(address="test_1")
    defender = Player(address="test_2")
    players = [attacker, defender]
    rule.setup(players)
    attacker.drop_cards()
    defender.drop_cards()

    attack_card = Card(rank=attack_rank, suit=SuitEnum.D)
    defend_card = Card(rank=defend_rank, suit=SuitEnum.D)
    attacker.take_card(attack_card)
    defender.take_card(defend_card)
    rule.turn_of_player = (attacker, attack_card)

    assert rule.attack(attack_card, defender) == attack_card
    assert rule.turn_of_player == (attacker, attack_card) if defend_rank < attack_rank else (defender, attack_card)


def test_durak_rule_defend():
    deck = ShortDeck()
    rule = DurakRule(deck)
    attacker = Player(address="test_1")
    defender = Player(address="test_2")
    players = [attacker, defender]
    rule.setup(players)
    attacker.drop_cards()
    defender.drop_cards()

    rule.trump = Card(rank=6, suit=SuitEnum.D)
    attack_card = Card(rank=10, suit=SuitEnum.D)
    defend_card = Card(rank=11, suit=SuitEnum.D)
    attacker.take_card(attack_card)
    defender.take_card(defend_card)
    rule.turn_of_player = (attacker, attack_card)
    rule.attack(attack_card, defender)

    rule.defend(defend_card, attacker)


@pytest.mark.parametrize("hand, board, expected", [
    (
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 2, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.D},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            [
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 13, "suit": SuitEnum.D}
            ]
    ),
    (
            [
                {"rank": 5, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 2, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 14, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.C},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            [
                {"rank": 5, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 13, "suit": SuitEnum.C},
                {"rank": 5, "suit": SuitEnum.C}
            ],
    ),
    (
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.D},
                {"rank": 6, "suit": SuitEnum.C}
            ],
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 13, "suit": SuitEnum.D},
            ]
    ),
    (
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 6, "suit": SuitEnum.H}
            ],
            [
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.C}
            ],
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 6, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 6, "suit": SuitEnum.C}

            ]
    ),
    (
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 10, "suit": SuitEnum.C}
            ],
            [
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.S},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.C}
            ],
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 10, "suit": SuitEnum.C},
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.S},
            ]
    ),
    (
            [
                {"rank": 2, "suit": SuitEnum.D},
                {"rank": 3, "suit": SuitEnum.C}
            ],
            [
                {"rank": 4, "suit": SuitEnum.H},
                {"rank": 5, "suit": SuitEnum.S},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 13, "suit": SuitEnum.H},
                {"rank": 7, "suit": SuitEnum.C}
            ],
            []
    )
])
def test_get_combo_by_set(hand, board, expected):
    deck = ShortDeck()
    rule = HoldEmPokerRule(deck)
    hand = [Card(**data) for data in hand]
    board = [Card(**data) for data in board]
    assert rule._get_combo_by_set_combo(hand, board) == [Card(**data) for data in expected]


@pytest.mark.parametrize("hand, board, expected, params", [
    (
            [
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 9, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 12, "suit": SuitEnum.H},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            [
                {"rank": 9, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 12, "suit": SuitEnum.H},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            {"flash": 1, "royal": 1, "straight": 1}
    ),
    (
            [
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 9, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 12, "suit": SuitEnum.D},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            [
                {"rank": 9, "suit": SuitEnum.H},
                {"rank": 10, "suit": SuitEnum.D},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 12, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            {"flash": 0, "royal": 0, "straight": 1}
    ),
    (
            [
                {"rank": 14, "suit": SuitEnum.D},
                {"rank": 2, "suit": SuitEnum.H}
            ],
            [
                {"rank": 3, "suit": SuitEnum.H},
                {"rank": 4, "suit": SuitEnum.H},
                {"rank": 5, "suit": SuitEnum.S},
                {"rank": 12, "suit": SuitEnum.D},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            [
                {"rank": 14, "suit": SuitEnum.D},
                {"rank": 2, "suit": SuitEnum.H},
                {"rank": 3, "suit": SuitEnum.H},
                {"rank": 4, "suit": SuitEnum.H},
                {"rank": 5, "suit": SuitEnum.S}
            ],
            {"flash": 0, "royal": 0, "straight": 1}
    ),
    (
            [
                {"rank": 2, "suit": SuitEnum.D},
                {"rank": 13, "suit": SuitEnum.H}
            ],
            [
                {"rank": 9, "suit": SuitEnum.H},
                {"rank": 11, "suit": SuitEnum.H},
                {"rank": 6, "suit": SuitEnum.S},
                {"rank": 12, "suit": SuitEnum.D},
                {"rank": 5, "suit": SuitEnum.C}
            ],
            None,
            None
    ),

])
def test_get_combo_by_sequence(hand, board, expected, params):
    deck = ShortDeck()
    rule = HoldEmPokerRule(deck)
    hand = [Card(**data) for data in hand]
    board = [Card(**data) for data in board]
    if expected:
        assert rule._get_combo_by_sequence(hand, board) == {"combo": [Card(**data) for data in expected], **params}
    else:
        assert not rule._get_combo_by_sequence(hand, board)
