from loguru import logger
from sqlite3 import connect as sqlite3_connect, Error as SQLiteError
from .sqlite_manages import SqliteCursorManages
from src.configs import DB_PATH


class DataBaseSQLite3:
    """ База данных SQLite3. """

    __slots__ = ("connection",)

    def __init__(self) -> None:
        self.connection = None
        self.connect()

    def connect(self) -> None:
        """ Подключение к БД. """
        try:
            self.connection = sqlite3_connect(DB_PATH)
            logger.success("Successful connection to the Data Base!")
        except SQLiteError as error:
            logger.error(error)

    # @is_connection_check(message=N.CONNECTION_PROBLEMS)
    def save(self, data: tuple | list) -> None:
        """ Сохранение данных в БД. """
        with SqliteCursorManages(self.connection) as cursor:
            # cursor.execute(Q.INSERT_USER % (*data,))
            pass
        self.connection.commit()

    # @is_connection_check(message=N.CONNECTION_PROBLEMS)
    def read(self) -> tuple | list:
        """ Чтение данных из БД. """
        with SqliteCursorManages(self.connection) as cursor:
            # cursor.execute(Q.SELECT_USERS)
            # return [item for item in cursor.fetchall()]
            return []

    def __del__(self):
        """ Разрываем соединение с базой. """
        if self.connection is not None:
            self.connection.close()
