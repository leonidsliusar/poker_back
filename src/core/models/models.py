"""src.core.models.models."""
from enum import Enum

from pydantic import BaseModel, field_validator

from src.core.cards.card_enum import SuitEnum
from src.core.player.payable_player import PayablePlayer


class HoldemStageEnum(str, Enum):
    INIT: str = "start_deal"
    FLOP: str = "flop"
    TURN: str = "turn"
    RIVER: str = "river"
    END: str = "end_deal"


class ActionEnum(str, Enum):
    RAISE: str = "raise_"
    CALL: str = "call"
    CHECK: str = "check"
    FOLD: str = "fold"


class Card(BaseModel):
    suit: SuitEnum
    rank: int


class ProcedureEnum(str, Enum):
    JOIN: str = "add_player"
    START: str = "start_deal"
    MOVE: str = "make_move"
    COMPLETE: str = "complete_turn"


class PlayerModel(BaseModel):
    address: str
    hand: list[Card | None] = []
    name: str | None = None
    idx: int | None = None
    action: ActionEnum | None = None


class PayablePlayerModel(PlayerModel):
    balance: int
    amount: int | None = None


class RequestModel(BaseModel):
    command: ProcedureEnum
    player: PayablePlayerModel | None = None

    def get_player(self) -> PayablePlayer:
        return PayablePlayer(address=self.player.address)


class Response(BaseModel):
    player: PayablePlayerModel
    bet: int
    player_last_bet: int
    excluded_actions: ActionEnum | None = None

    @field_validator("player", mode="before")
    @classmethod
    def transform_player(cls, player: PayablePlayer) -> PayablePlayerModel:
        return PayablePlayerModel.model_validate(player, from_attributes=True)


class WinnerResponse(BaseModel):
    players: list[PayablePlayerModel]
