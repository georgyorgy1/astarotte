import sqlite3

import lib.logger as logger


class Database:
    def __init__(self):
        self.__database_file_name = 'astarotte.db'
        self.__logger = logger.Logger('database.py')

    def __create_connection(self):
        try:
            return sqlite3.connect(self.__database_file_name)
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
        return None

    def __close_connection(self, connection):
        try:
            connection.close()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)

    def retrieve_single_result(self, statement, parameters):
        try:
            connection = self.__create_connection()
            cursor = connection.cursor()
            cursor.execute(statement, parameters)
            return cursor.fetchone()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
        finally:
            self.__close_connection(connection)



