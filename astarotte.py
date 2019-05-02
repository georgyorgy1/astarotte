import bot
import lib.jsonfile as jsonfile
import lib.logger as logger


class Astarotte:
    def __init__(self):
        self._client = bot.Bot()
        self._json_file = jsonfile.JSONFile('config.json')
        self._bot_config = self._json_file.get_json_file()
        self._token = self._bot_config['token']
        self._logger = logger.Logger('astarotte.py')

    def main(self):
        self._logger.log_info('Starting AstarotteBot...')
        self._client.start_bot(self._token)


if __name__ == '__main__':
    astarotte = Astarotte()
    astarotte.main()

