import logging


class Logger:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__log_format = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')

    def __get_file_handler(self, log_format):
        file_handler = logging.FileHandler('astarotte.log')
        file_handler.setFormatter(log_format)
        return file_handler

    def __get_stream_handler(self, log_format):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        return stream_handler

    def __get_logger(self, level):
        logger = logging.getLogger(self.__file_name)
        if not logger.handlers: # Prevents duplicate log entries
            logger.setLevel(level)
            logger.addHandler(self.__get_file_handler(self.__log_format))
            logger.addHandler(self.__get_stream_handler(self.__log_format))
        return logger

    def log_info(self, event):
        self.__get_logger(logging.INFO).info(event)

    def log_error(self, event):
        self.__get_logger(logging.ERROR).error(event)

    def log_warn(self, event):
        self.__get_logger(logging.WARNING).warning(event)

