import os
import yaml


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(object):

    def __init__(self, name):
        self.path = os.path.join(BASE_DIR, 'data/%s.yaml' % name)

    def __call__(self):
        with open(self.path) as f:
            config = yaml.load(f)
        return config
