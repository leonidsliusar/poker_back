from src.core.deck.deck import ShortDeck
from src.core.games.durak.rule import DurakRule
from src.core.player.player import Player
from src.core.state.durakstate import DurakState


def test_state():
    deck = ShortDeck()
    rule = DurakRule(deck)
    state = DurakState(rule)
    player_1 = Player(address="test_1")
    player_2 = Player(address="test_2")
    state.add_player(player_1)
    state.add_player(player_2)
    assert state.players == [player_1, player_2]
    state.start()
    assert len(player_1.hand) == 6
    assert len(player_2.hand) == 6
    assert player_1.name == "Player 1"
    assert player_2.name == "Player 2"
    assert player_1.idx == 0
    assert player_2.idx == 1
    assert rule.trump
    assert rule.turn_of_player
