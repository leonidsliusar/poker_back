from core.desks.abstract.table import AbstractTable


class ClassicTable(AbstractTable):
    """Classic Table with 6 players limit."""

    max_players: int = 6

