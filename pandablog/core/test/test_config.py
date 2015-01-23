__author__ = 'TwIStOy'

import unittest
from pandablog.core import Config
import codecs
import json
import os


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config_info = {
            "default_author": "TwIStOy",
            "default_category": "test",
            "default_title": "hello world",
            "default_datetime": "2012-12-12"
        }
        with codecs.open('c:\\config.json', "w", "utf-8") as fp:
            json.dump(self.config_info, fp)

    def tearDown(self):
        if os.path.isfile('c:\\config.json'):
            os.remove("c:\\config.json")

    def test_all(self):
        global_config = Config.Config('c:\\config.json')
        global_config.load()
        for k, v in self.config_info.iteritems():
            self.assertEqual(getattr(global_config, k), v)
            self.assertEqual(global_config.get(k), v)


if __name__ == '__main__':
    unittest.main()
