import pytest

from core.cards.card import Card
from core.cards.card_enum import SuitEnum
from core.deck.deck import ShortDeck
from core.games.durak.rule import DurakRule
from core.player.player import Player


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


