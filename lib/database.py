import sqlite3

import lib.logger as logger


class Database:
    def __init__(self):
        self.__database_file_name = 'astarotte.db'
        self.__logger = logger.Logger('database.py')

    def create_connection(self):
        try:
            return sqlite3.connect(self.__database_file_name)
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)
        return None

    def close_connection(self, connection):
        try:
            connection.close()
        except sqlite3.Error as exception:
            self.__logger.log_error(exception)

