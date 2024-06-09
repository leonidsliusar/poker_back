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
