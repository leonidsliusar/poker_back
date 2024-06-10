"""core.games.durak.rule."""
from core.cards.abstract.card import AbstractCard
from core.deck.abstract.deck import AbstractDeck
from core.games.abstract.rule import AbstractRule
from core.player.abstract.player import AbstractPlayer


class DurakRule(AbstractRule):
    max_players: int = 6
    min_players: int = 2
    max_deck_size: int = 52
    min_deck_size: int = 36
    init_card_quantity: int = 6
    round_quantity: None = None
    deck: AbstractDeck
    _trump: AbstractCard | None = None
    _turn_of_player: tuple[AbstractPlayer, AbstractCard] | None = None

    @property
    def trump(self) -> AbstractCard | None:
        return self._trump

    @trump.setter
    def trump(self, card: AbstractCard):
        self._trump = card

    @trump.deleter
    def trump(self):
        self._trump = None

    @property
    def turn_of_player(self) -> tuple[AbstractPlayer, AbstractCard]:
        return self._turn_of_player

    @turn_of_player.setter
    def turn_of_player(self, data: tuple[AbstractPlayer, AbstractCard]):
        if self.turn_of_player and self.turn_of_player[1] < data[1]:
            self._turn_of_player = data
        else:
            self._turn_of_player = data

    def setup(self, players: list[AbstractPlayer]):
        self.deck.shuffle()
        self.trump = self.deck.card
        self._dealt(players)

    def _dealt(self, players: list[AbstractPlayer]):
        for i in range(self.init_card_quantity):
            for player in players:
                card = self.deck.card
                if card.same_suit(self.trump):
                    self.turn_of_player = (player, card)
                player.take_card(card)

    def attack(self, card: AbstractCard, next_player: AbstractPlayer) -> AbstractCard:
        attacker = self.turn_of_player[0]
        card_from_hand = attacker.turn(card)
        if self.is_defendable(attack_card=card, defender=next_player):
            self.turn_of_player = (next_player, card_from_hand)
        else:
            self.turn_of_player = (self.turn_of_player[0], card_from_hand)
        return card_from_hand

    def defend(self, card: AbstractCard, next_player: AbstractPlayer) -> AbstractCard | None:
        defender = self.turn_of_player[0]
        card_from_hand = defender.turn(card)
        attack_card = self.turn_of_player[1]
        defend_card = None
        if not self.is_defended(card_from_hand, attack_card):
            defender.take_card(attack_card)
        else:
            defend_card = card_from_hand
        self.turn_of_player = (next_player, card_from_hand)
        return defend_card

    def is_defendable(self, attack_card: AbstractCard, defender: AbstractPlayer) -> bool:
        defendable = []
        for card in defender.hand:
            defendable.append(self.is_defended(defend_card=card, attack_card=attack_card))
        return any(defendable)

    def is_defended(self, defend_card: AbstractCard, attack_card: AbstractCard) -> bool:
        if self.is_trump(defend_card) and not self.is_trump(attack_card):
            return True
        return defend_card > attack_card

    def is_trump(self, card: AbstractCard) -> bool:
        return self.trump.same_suit(card)

