"""src.dispatcher."""
from src.core.models.models import RequestModel, ProcedureEnum
from src.core.state.abstract.state import AbstractState


class Dispatcher:

    _state: AbstractState | None

    def __init__(self, state: AbstractState):
        self._state = state

    @property
    def state(self) -> AbstractState:
        return self._state

    def exec(self, request: RequestModel):
        state = self.state
        func = getattr(state, request.command)
        if request.player:
            match request.command:
                case ProcedureEnum.MOVE:
                    result = func(
                        player_idx=request.player.idx,
                        action=request.player.action,
                        amount=request.player.amount
                    )
                case _:
                    result = func(request.get_player())
        else:
            result = func()
        return result
