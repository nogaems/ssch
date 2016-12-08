from utils import *
import json
import logging as log
import datetime

proxies = {}


class Sosuch:
    boards_url = 'https://2ch.hk/makaba/mobile.fcgi?task=get_boards'
    boards = {}

    def __init__(self):
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.ERROR)
        self.load()

    def load(self):
        try:
            response = get_request(self.boards_url, proxies)
        except SosuchRequestError as e:
            exit(1)
        self.boards_settings = json.loads(response.text)
        self.categories = list(self.boards_settings.keys())
        self.boards = {}
        for category in self.categories:
            for config in self.boards_settings[category]:
                self.boards[config['id']] = Board(config)


class Board:
    loaded = False

    def __init__(self, config):
        self.id = config['id']
        self.name = config['name']
        self.default_name = config['default_name']
        self.enable_posting = bool(config['enable_posting'])
        self.bump_limit = int(config['bump_limit'])
        self.category = config['category']

    def __str__(self):
        return '/{}/ — {}'.format(self.id, self.name)

    def __repr__(self):
        return self.__str__()

    def load(self):
        if not self.loaded:
            self.refresh()
            loaded = True

    def refresh(self, page=0):
        page_url = 'https://2ch.hk/{}/threads.json'.format(self.id)
        try:
            response = get_request(page_url, proxies)
        except SosuchRequestError as e:
            exit(1)
        self.threads = []
        for thread in json.loads(response.text)['threads']:
            self.threads.append(Thread(thread))


class Thread:
    posts = []

    def __init__(self, op):
        self.comment = op['comment']
        self.lasthit = op['lasthit']
        self.num = op['num']
        self.posts_count = int(op['posts_count'])
        self.score = float(op['score'])
        self.subject = op['subject']
        self.timestamp = int(op['timestamp'])
        self.views = int(op['views'])
        self.created = datetime.datetime.fromtimestamp(
            self.timestamp).strftime('%D %A %H:%M:%S')

    def __str__(self):
        return '{} — {}'.format(self.subject, self.created)

    def __repr__(self):
        return self.__str__()


class Post:

    def __init__(self, post):
        pass

sosuch = Sosuch()
sosuch.boards['b'].load()
print(sosuch.boards['b'].threads)
