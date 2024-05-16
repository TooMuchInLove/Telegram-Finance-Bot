from sqlite3 import Cursor, Connection


class SqliteCursorManages:
    """ Контекстный менеджер для усправления курсором SQLite3. """

    __slots__ = ("__connection", "__cursor",)

    def __init__(self, connection: Connection) -> None:
        self.__connection = connection

    def __enter__(self) -> Cursor:
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.__cursor.close()
