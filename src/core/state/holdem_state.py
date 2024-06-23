from contextlib import contextmanager

from src.core.cards.abstract.card import AbstractCard
from src.core.models.models import HoldemStageEnum, Response, WinnerResponse, ActionEnum
from src.core.player.payable_player import PayablePlayer
from src.core.state.abstract.state import AbstractState
from src.core.games.texas_holdem.rule import HoldEmPokerRule
from collections import deque


class HoldemState(AbstractState):
    _players: deque[PayablePlayer | None]
    _out_players: list[PayablePlayer | None]
    _player_bets: dict[PayablePlayer, int] | None
    rule: HoldEmPokerRule
    _current_board: list[AbstractCard | None]
    _start_deal_player_idx: int = 0
    _deal_counter: int = 0
    _current_bet: int = 0
    _current_stage: HoldemStageEnum

    def __init__(self, rule: HoldEmPokerRule):
        super().__init__(rule=rule)
        self._current_board = []
        self._out_players = []
        self._player_bets = {}
        self._players = deque(maxlen=rule.max_players)

    @property
    def out_players(self) -> list[PayablePlayer]:
        return self._out_players

    def add_to_out_players(self, player: PayablePlayer):
        self.out_players.append(player)

    @property
    def start_deal_player(self) -> int:
        return self._start_deal_player_idx

    def increment_start_deal_player(self):
        self._start_deal_player_idx += 1

    @property
    def stage(self) -> HoldemStageEnum:
        return self._current_stage

    @stage.setter
    def stage(self, stage: HoldemStageEnum):
        self._current_stage = stage

    @property
    def deal_counter(self) -> int:
        return self._deal_counter

    def increment_deal_counter(self):
        self._deal_counter += 1

    def add_player_bet(self, player: PayablePlayer, bet: int):
        self._player_bets[player] = bet

    def get_player_bet(self, player: PayablePlayer) -> int:
        return self._player_bets.get(player, 0)

    def all_bet_is_called(self) -> bool:
        max_bet = max(self._player_bets.values())
        for player, bet in self._player_bets.items():
            if bet != max_bet:
                return False
        return True

    @property
    def players(self) -> deque[PayablePlayer]:
        return self._players

    @players.setter
    def players(self, players: deque[PayablePlayer]):
        self._players = players

    def add_player(self, player: PayablePlayer):
        """Interface for adding player in game"""
        player.idx = len(self.players)
        self.players.append(player)
        player.name = f"Player {len(self.players)}"

    def start_deal(self) -> Response:
        """Interface for starting deal(round). Stage - INIT"""
        if len(self.players) >= self.rule.min_players:
            self.rule.setup(list(self.players))
            self._init_turn()
            player_bet = self.get_player_bet(self.current_player)
            current_bet = self.rule.bet
            excluded_actions = self.get_excluded_action(current_bet, player_bet)
            self.stage = HoldemStageEnum.INIT
            return Response(
                player=self.current_player,
                bet=current_bet,
                player_last_bet=player_bet,
                excluded_actions=excluded_actions,
            )

    def flop(self):
        """Interface for doing flop stage. Stage - FLOP"""
        if len(self.players) >= self.rule.min_players:
            cards = self.rule.flop()
            for card in cards:
                self.push_to_current_board(card)
            return Response(
                player=self.current_player,
                bet=0,
                player_last_bet=0,
            )

    def turn(self):
        """Interface for doing turn stage. Stage - TURN"""
        if len(self.players) >= self.rule.min_players:
            card = self.rule.turn()
            self.push_to_current_board(card)
            return Response(
                player=self.current_player,
                bet=0,
                player_last_bet=0,
            )

    def river(self):
        """Interface for doing river stage. Stage - RIVER"""
        if len(self.players) >= self.rule.min_players:
            card = self.rule.river()
            self.push_to_current_board(card)
            return Response(
                player=self.current_player,
                bet=0,
                player_last_bet=0,
            )

    def end_deal(self) -> WinnerResponse:
        """Interface for ending deal(round). Stage - END.
        Getting winners, moving players from out, clearing current_board and hands, sorting players, overloading deck
        and starting dealing.
        """
        # TODO: Add implementation of getting winner/s by combination
        winners = []
        self._move_player_from_out()
        self._clear_board()
        self._clear_hands()
        self._sort_players()
        self.rule.reload_deck()
        return WinnerResponse(players=winners)

    def _move_player_from_out(self):
        for player in self._out_players:
            self.players.append(player)

    def _clear_board(self):
        self._current_board.clear()

    def _clear_hands(self):
        for player in self.players:
            player.drop_cards()

    def _sort_players(self):
        self.increment_start_deal_player()
        player = self.players.popleft()
        while player.idx != self.start_deal_player:
            self.players.append(player)
            player = self.players.popleft()
        self.players.appendleft(player)
        players_array = list(self.players)
        players_array.sort(key=lambda player_item: player_item.idx)
        self.players = deque(players_array)

    def make_move(self, player_idx: int, action: ActionEnum, amount: int | None = None) -> Response:
        """Interface for make move(do an action)"""
        if player_idx == self.current_player.idx:
            action_method = getattr(self.rule, action)
            with self.current_player_set_in_end() as player:
                match action:
                    case ActionEnum.CALL:
                        amount = self.rule.bet  # TODO: move bet to State
                    case ActionEnum.FOLD:
                        amount = None
                action_method(player, amount)
            """...Next player..."""
            player_bet = self.get_player_bet(self.current_player)
            current_bet = self.rule.bet
            excluded_actions = self.get_excluded_action(current_bet, player_bet)
            return Response(
                player=self.current_player,
                bet=current_bet,
                player_last_bet=player_bet,
                excluded_actions=excluded_actions,
            )

    def complete_turn(self):
        if self.all_bet_is_called():
            return self._next_stage()

    def _next_stage(self):
        match self.stage:
            case HoldemStageEnum.INIT:
                self.stage = HoldemStageEnum.FLOP
            case HoldemStageEnum.FLOP:
                self.stage = HoldemStageEnum.TURN
            case HoldemStageEnum.TURN:
                self.stage = HoldemStageEnum.RIVER
            case HoldemStageEnum.RIVER:
                self.stage = HoldemStageEnum.END
            case HoldemStageEnum.END:
                self.stage = HoldemStageEnum.INIT
        return getattr(self, self.stage.value)()

    @staticmethod
    def get_excluded_action(current_bet: int, player_bet: int) -> ActionEnum | None:
        if current_bet > player_bet:
            return ActionEnum.CHECK

    def _init_turn(self):
        """Make a blinds"""
        with self.current_player_set_in_end() as player:
            self.rule.small_blind(player)
            self.add_player_bet(player=player, bet=self.rule.blind // 2)
        with self.current_player_set_in_end() as player:
            self.rule.big_blind(player)
            self.add_player_bet(player=player, bet=self.rule.blind)

    @property
    def current_player(self) -> PayablePlayer:
        """Return current player"""
        return self.players[0]

    @contextmanager
    def current_player_set_in_end(self) -> PayablePlayer:
        """Take the first player and put it at the end of queue."""
        player = self.players.popleft()
        yield player
        if player.hand:
            self.players.append(player)
        else:
            self.add_to_out_players(player)

    def push_to_current_board(self, card: AbstractCard):
        self._current_board.append(card)

    def clear_current_board(self):
        self._current_board.clear()

    def end_turn(self):
        self.clear_current_board()
