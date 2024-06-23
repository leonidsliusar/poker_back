from src.core.player.abstract.player import AbstractPlayer


class PayablePlayer(AbstractPlayer):
    _balance: int

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, amount: int):
        self._balance = amount

    def increase_balance(self, amount: int):
        self._balance += amount

    def decrease_balance(self, amount: int):
        self._balance -= amount
