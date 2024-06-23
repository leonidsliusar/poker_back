from abc import ABC, abstractmethod

from core.desks.abstract.table import AbstractTable


class TableFactory(ABC):
    tables: dict = {}

    @abstractmethod
    def get_table(self) -> AbstractTable:
        ...
