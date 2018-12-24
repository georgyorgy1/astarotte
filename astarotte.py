import bot
import lib.jsonfile as jsonfile
import lib.logger as logger


class Astarotte:
    def __init__(self):
        self.__client = bot.Bot()
        self.__json_file = jsonfile.JSONFile('config.json')
        self.__bot_config = self.__json_file.get_json_file()
        self.__token = self.__bot_config['token']
        self.__logger = logger.Logger('astarotte.py')

    def main(self):
        self.__logger.log_info('Starting AstarotteBot...')
        self.__client.start_bot(self.__token)


if __name__ == '__main__':
    astarotte = Astarotte()
    astarotte.main()

