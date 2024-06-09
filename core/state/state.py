from enum import Enum

from core.cards.abstract.card import AbstractCard
from core.games.durak.rule import DurakRule
from core.player.abstract.player import AbstractPlayer
from core.state.abstract.state import AbstractState


class DurakStateEnum(str, Enum):
    A: str = "Attack"
    D: str = "Defend"


class State(AbstractState):
    rule: DurakRule
    _current: DurakStateEnum = DurakStateEnum.A

    def turn(self, card: AbstractCard):
        match self.current:
            case DurakStateEnum.A:
                card = self.rule.attack(card, self.next_player)
            case DurakStateEnum.D:
                card = self.rule.defend(card, self.next_player)
        self.switch_current_state()
        return card

    @property
    def next_player(self) -> AbstractPlayer:
        attacker_idx = self.rule.turn_of_player[0].idx
        return self.players[attacker_idx + 1]

    @property
    def current(self) -> str:
        return self._current

    @current.setter
    def current(self, current: DurakStateEnum):
        self._current = current

    def switch_current_state(self):
        if self.current == DurakStateEnum.A:
            self.current = DurakStateEnum.D
        else:
            self.current = DurakStateEnum.A
