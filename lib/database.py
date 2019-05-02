import sqlite3

import lib.logger as logger


class Database:
    def __init__(self):
        self._logger = logger.Logger('database.py')

    def _create_connection(self):
        try:
            return sqlite3.connect('astarotte.db')
        except sqlite3.Error as exception:
            self._logger.log_error(exception)
        return None

    def _close_cursor(self, cursor):
        try:
            cursor.close()
        except sqlite3.Error as exception:
            self._logger.log_error(exception)

    def _close_connection(self, connection):
        try:
            connection.close()
        except sqlite3.Error as exception:
            self._logger.log_error(exception)

    def execute_update(self, statement, parameters):
        try:
            connection = self._create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            connection.commit()
            success = True
        except sqlite3.Error as exception:
            self._logger.log_error(exception)
            success = False
        finally:
            self._close_cursor(cursor)
            self._close_connection(connection)
        return success

    def execute_query(self, statement, parameters):
        try:
            connection = self._create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            result = cursor.fetchall()
        except sqlite3.Error as exception:
            self._logger.log_error(exception)
            result = None
        finally:
            self._close_cursor(cursor)
            self._close_connection(connection)
        return result



