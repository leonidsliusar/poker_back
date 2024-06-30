"""core.games.texas-holdem.rule."""
from collections import OrderedDict

from src.core.cards.abstract.card import AbstractCard
from src.core.cards.card_enum import HigherRankEnum
from src.core.deck.deck import LongDeck
from src.core.exceptions.exceptions import ComboError
from src.core.games.abstract.rule import AbstractRule
from src.core.player.abstract.player import AbstractPlayer
from src.core.player.payable_player import PayablePlayer


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
        self._current_blind = kwargs.pop("init_blind", 2)
        self._INIT_CHIPS = kwargs.pop("init_chips", 5000)
        self.deck.shuffle()
        self._dealt(players)

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

    def get_winners(self, players: list[PayablePlayer], board: list[AbstractCard]) -> list[PayablePlayer]:
        players_rank = OrderedDict()
        for player in players:
            rank = self._get_rank_of_combo(player.hand, board)
            players_rank[player.idx] = rank
        sorted_players_rank = OrderedDict(sorted(players_rank.items(), key=lambda item: item[1], reverse=True))
        winners_idx = []
        winners_rank = 0
        for player_idx, rank in sorted_players_rank.items():
            if rank >= winners_rank:
                winners_idx.append(player_idx)
        return [player for player in players if players.index(player) in winners_idx]

    def _get_rank_of_combo(self, hand: list[AbstractCard], board: list[AbstractCard]) -> int:
        set_combo = self._get_combo_by_set_combo(hand, board)
        sequence_combo = self._get_combo_by_sequence(hand, board)
        kicker = self._get_kicker(hand, board)
        rank = self._get_combo_rank(set_combo, sequence_combo, kicker)
        return rank

    def _get_combo_rank(
            self,
            set_combo: list[AbstractCard | None],
            sequence_combo: dict[str, list[AbstractCard] | int] | None,
            kicker: AbstractCard
    ) -> int:
        set_rank = 0
        sequence_rank = 0
        if set_combo:
            set_rank = self._get_rank_by_set_combo(set_combo)
        if sequence_combo:
            sequence_rank = self._get_rank_by_sequence_combo(sequence_combo)
        rank = set_rank if set_rank > sequence_rank else sequence_rank
        rank += kicker.rank
        return rank

    @staticmethod
    def _get_rank_by_set_combo(set_combo: list[AbstractCard]) -> int:
        length_of_combo = len(set_combo)
        if length_of_combo == 2:  # pair
            return 1
        elif length_of_combo == 3:  # three of a kind
            return 3
        elif length_of_combo == 4:
            if len({card.rank for card in set_combo}) == 2:  # two pair
                return 2
            elif len({card.rank for card in set_combo}) == 1:  # four of a kind
                return 7
        elif length_of_combo == 5:  # full house
            return 6
        else:
            raise ComboError(set_combo)

    @staticmethod
    def _get_rank_by_sequence_combo(sequence_combo: dict[str, list[AbstractCard] | int] | None) -> int:
        royal = sequence_combo.get("royal")
        flash = sequence_combo.get("flash")
        straight = sequence_combo.get("straight")
        if royal:
            return 9  # royal flash
        elif flash and straight:
            return 8  # straight flash
        elif flash:
            return 5  # flash
        elif straight:
            return 4  # straight
        else:
            raise ComboError(sequence_combo.get("combo"))

    def _get_combo_by_set_combo(self, hand: list[AbstractCard], board: list[AbstractCard]) -> list[AbstractCard | None]:
        """Checks that user combo is pair, two pair, three of a kind or four of a kind."""
        counter = OrderedDict()
        cards = hand + board
        for board_card in cards:
            if counter.get(board_card.rank):
                counter[board_card.rank] += 1
            else:
                counter[board_card.rank] = 1
        sorted_counter = OrderedDict(
            sorted(
                counter.items(),
                key=lambda item: (-item[1], -item[0])
            )
        )
        ordered_combo_map = OrderedDict(list(sorted_counter.items())[:2])
        self._remove_if_four_of_kind(ordered_combo_map)
        combo_map = dict(ordered_combo_map)
        combo = []
        for card in cards:
            if card.rank in combo_map:
                if combo_map[card.rank] > 1:
                    combo.append(card)
        return combo

    @staticmethod
    def _remove_if_four_of_kind(combo_map: OrderedDict[int, int]):
        to_remove = 0
        for rank, count in combo_map.items():
            if count == 4:
                to_remove = 1
            elif to_remove:
                combo_map.pop(rank)

    def _get_combo_by_sequence(
            self,
            hand: list[AbstractCard],
            board: list[AbstractCard]
    ) -> dict[str, list[AbstractCard] | int] | None:
        cards = hand + board
        straight_combo_ace_max = self._get_straight_combo(cards)
        straight_combo_ace_min = self._get_straight_combo(cards)
        flash_combo = self._get_flash_combo(cards)
        if flash_combo and straight_combo_ace_max:
            combo = {"combo": flash_combo, "royal": 1, "flash": 1, "straight": 1}
        elif flash_combo and straight_combo_ace_min:
            combo = {"combo": flash_combo, "royal": 0, "flash": 1, "straight": 1}
        elif flash_combo:
            combo = {"combo": flash_combo, "royal": 0, "flash": 1, "straight": 0}
        elif straight_combo_ace_max:
            combo = {"combo": straight_combo_ace_max, "royal": 0, "flash": 0, "straight": 1}
        elif straight_combo_ace_min:
            combo = {"combo": straight_combo_ace_min, "royal": 0, "flash": 0, "straight": 1}
        else:
            combo = None
        return combo

    def _get_straight_combo(self, cards: list[AbstractCard]) -> list[AbstractCard | None]:
        cards.sort(key=lambda item: (item.rank, item.suit))
        last_seq_value = None
        to_combo = []
        for card in cards:
            if last_seq_value:
                if last_seq_value + 1 == card.rank:
                    to_combo.append(card)
                else:
                    if len(to_combo) < 5:
                        to_combo.clear()
                        to_combo.append(card)
                    else:
                        break
            else:
                to_combo.append(card)
            last_seq_value = card.rank
        if len(to_combo) < 5:
            to_combo.clear()
        self._switch_ace_rank(cards)
        return to_combo

    @staticmethod
    def _switch_ace_rank(cards: list[AbstractCard]):
        for card in cards:
            if card.rank == HigherRankEnum.highest():
                card.rank = 1
            elif card.rank == 1:
                card.rank = HigherRankEnum.highest()

    @staticmethod
    def _get_flash_combo(cards: list[AbstractCard]) -> list[AbstractCard | None]:
        cards.sort(key=lambda item: item.suit)
        last_seq_value = None
        to_combo = []
        for card in cards:
            if last_seq_value:
                if last_seq_value == card.suit:
                    to_combo.append(card)
                else:
                    if len(to_combo) < 5:
                        to_combo.clear()
                        to_combo.append(card)
                    else:
                        break
            else:
                to_combo.append(card)
            last_seq_value = card.suit
        if len(to_combo) < 5:
            to_combo.clear()
        return to_combo

    @staticmethod
    def _get_kicker(hand: list[AbstractCard], board: list[AbstractCard]) -> AbstractCard:
        """Returns kicker."""
        kicker = None
        cards = hand + board
        for card in cards:
            if not kicker:
                kicker = card
            elif kicker < card:
                kicker = card
        return kicker
