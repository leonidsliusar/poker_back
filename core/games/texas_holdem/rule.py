"""core.games.texas-holdem.rule."""
from core.cards.abstract.card import AbstractCard
from core.deck.deck import LongDeck
from core.games.abstract.rule import AbstractRule
from core.player.abstract.player import AbstractPlayer
from core.player.payable_player import PayablePlayer


class HoldEmPokerRule(AbstractRule):
    _MAX_PLAYERS: int = 6
    _MIN_PLAYERS: int = 2
    _MAX_DECK_SIZE: int = 52
    _MIN_DECK_SIZE: int = 52
    _INIT_CARD_QUANTITY: int = 2
    _INIT_CHIPS: int
    _current_blind: int
    _blind_step: int = 2
    _current_dealt: int = 1
    _current_bet: int = 0
    deck: LongDeck

    def setup(self, players: list[AbstractPlayer], *args, **kwargs):
        self.deck.shuffle()
        self._dealt(players)
        self._current_blind = kwargs.pop("init_blind", 2)
        self._INIT_CHIPS = kwargs.pop("init_chips", 5000)

    @property
    def max_players(self) -> int:
        return self._MAX_PLAYERS

    @property
    def min_players(self) -> int:
        return self._MIN_PLAYERS

    def _dealt(self, players: list[AbstractPlayer]):
        for i in range(self._INIT_CARD_QUANTITY):
            for player in players:
                card = self.deck.card
                player.take_card(card)
                player.balance = self._INIT_CHIPS

    @property
    def blind(self) -> int:
        return self._current_blind

    @property
    def bet(self) -> int:
        return self._current_bet

    @bet.setter
    def bet(self, amount: int):
        self._current_bet = amount

    def small_blind(self, player: PayablePlayer):
        player.decrease_balance(self.blind // 2)

    def big_blind(self, player: PayablePlayer):
        player.decrease_balance(self.blind)
        self.bet = self.blind

    @staticmethod
    def check(player: PayablePlayer):
        pass

    @staticmethod
    def call(player: PayablePlayer, amount: int):
        player.decrease_balance(amount)

    @staticmethod
    def raise_(player: PayablePlayer, amount: int):
        player.decrease_balance(amount)

    @staticmethod
    def fold(player: PayablePlayer):
        player.drop_cards()

    def flop(self) -> list[AbstractCard]:
        cards = []
        for i in range(3):
            cards.append(self.deck.card)
        return cards

    def turn(self) -> AbstractCard:
        return self.deck.card

    def river(self) -> AbstractCard:
        return self.deck.card

    def get_winners(self) -> list[AbstractPlayer]:
        ...
