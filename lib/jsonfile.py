import json
import json.decoder

import lib.logger as logger


class JSONFile:
    def __init__(self, json_file_name):
        self.__logger = logger.Logger('config.py')
        self.__json_file_name = json_file_name

    def get_json_file(self):
        with open(self.__json_file_name, 'r') as json_raw_file:
            try:
                json_file = json.load(json_raw_file)
            except json.decoder.JSONDecodeError as exception:
                self.__logger.log_error(exception)
        return json_file
