import logging


class Logger:
    def __init__(self, file_name):
        self._file_name = file_name
        self._log_format = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')

    def _get_file_handler(self, log_format):
        file_handler = logging.FileHandler('astarotte.log')
        file_handler.setFormatter(log_format)
        return file_handler

    def _get_stream_handler(self, log_format):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        return stream_handler

    def _get_logger(self, level):
        logger = logging.getLogger(self._file_name)
        if not logger.handlers:
            logger.setLevel(level)
            logger.addHandler(self._get_file_handler(self._log_format))
            logger.addHandler(self._get_stream_handler(self._log_format))
        return logger

    def log_info(self, event):
        self._get_logger(logging.INFO).info(event)

    def log_error(self, event):
        self._get_logger(logging.ERROR).error(event)

    def log_warn(self, event):
        self._get_logger(logging.WARNING).warning(event)



