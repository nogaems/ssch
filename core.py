import json
import requests
import logging as log


class Sosuch:
    proxies = {}
    boards_url = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'

    def __init__(self):
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.ERROR)
        self.load()

    def load(self):
        try:
            response = requests.get(self.boards_url, proxies=self.proxies)
        except Exception as e:
            log.error('Internet connection issue: {}'.format(e))
            exit(1)
        if response.status_code != 200:
            log.error('Error: {} {}'.format(response.status_code,
                                            response.reason))
            exit(1)
        self.boards_settings = json.loads(response.text)
        self.categories = list(self.boards_settings.keys())
        self.boards = []
        for category in self.categories:
            for config in self.boards_settings[category]:
                self.boards.append(Board(config))


class Board:
    loaded = False

    def __init__(self, config):

        self.id = config['id']
        self.name = config['name']
        self.default_name = config['default_name']
        self.enable_posting = bool(config['enable_posting'])
        self.bump_limit = int(config['bump_limit'])
        self.category = config['category']
        self.pages_count = int(config['pages'])

        self.pages = [None] * self.pages_count

    def __str__(self):
        return '/{}/ — {}'.format(self.id, self.name)

    def __repr__(self):
        return self.__str__()

    def refresh(self, page=0):
        if


class Thread:
    pass


class Post:
    pass

sosuch = Sosuch()
