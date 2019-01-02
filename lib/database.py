import sqlite3

import lib.logger as logger


class Database:
    def __init__(self):
        self.__logger = logger.Logger('database.py')

    def __create_connection(self):
        try:
            return sqlite3.connect('astarotte.db')
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
        return None

    def __close_cursor(self, cursor):
        try:
            cursor.close()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)

    def __close_connection(self, connection):
        try:
            connection.close()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)

    def execute_update(self, statement, parameters):
        try:
            connection = self.__create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            connection.commit()
            success = True
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
            success = False
        finally:
            self.__close_cursor(cursor)
            self.__close_connection(connection)
        return success

    def execute_query(self, statement, parameters):
        try:
            connection = self.__create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            result = cursor.fetchall()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
            result = None
        finally:
            self.__close_cursor(cursor)
            self.__close_connection(connection)
        return result



