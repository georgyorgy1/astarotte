import json
import json.decoder

import lib.logger as logger


class JSONFile:
    def __init__(self, json_file_name):
        self._logger = logger.Logger('config.py')
        self._json_file_name = json_file_name

    def get_json_file(self):
        with open(self._json_file_name, 'r') as json_raw_file:
            try:
                json_file = json.load(json_raw_file)
            except json.decoder.JSONDecodeError as exception:
                self._logger.log_error(exception)
        return json_file

