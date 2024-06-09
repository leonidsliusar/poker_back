from core.desks.abstract.table_factory import TableFactory
from core.desks.table import ClassicTable


class ClassicTableFactory(TableFactory):

    def get_table(self) -> ClassicTable:
        table = ClassicTable()
        self.tables[table.id_] = table
        return table
