__author__ = 'TwIStOy'

import unittest
from pandablog.core import Loader
from pandablog.core import Util
from pandablog.core import Config
import codecs
import json
import os


class LoaderTest(unittest.TestCase):

    def test_all(self):
        global_config = Config.Config('c:\\panda\\config.json').load()
        loader = Loader.Loader('c:\\panda\\src', global_config)
        resource = loader.run()
        self.assertEqual(True, True)

    def setUp(self):
        # create a temporary source environment
        load_root_path = "c:\\panda\\src"
        Util.create_dir(load_root_path)
        Util.create_dir(Util.get_path(load_root_path, 'post'))
        Util.create_dir(Util.get_path(load_root_path, 'page'))
        Util.create_dir(Util.get_path(load_root_path, 'theme', 'default'))

        # make config.json at root folder
        with codecs.open("c:\\panda\\config.json", "w", "utf-8") as fp:
            config_info = {
                "default_author": "TwIStOy",
                "default_category": "test",
                "default_title": "hello world",
                "default_datetime": "2012-12-12",
                "theme": "default"
            }
            json.dump(config_info, fp)

        # make posts
        post_dict = {
            "post1.md": [
                'tags: a, b, c',
                'category: test',
                'author: test',
                'title: title_test',
                'datetime: 1000-1-1',
                "",
                "# a",
                "## aa"
            ],
            "post2.md": [
                'tags: a, b, c',
                'category: test',
                'author: test',
                'title: title_test',
                'datetime: 1000-1-1',
                "",
                "# a",
                "## aa"
            ],
            "post3.md": [
                'tags: a, b, c',
                'category: test',
                'author: test',
                'title: title_test',
                'datetime: 1000-1-1',
                "",
                "# a",
                "## aa"
            ]
        }
        for name, info in post_dict.items():
            with codecs.open('c:\\panda\\src\\post\\{}'.format(name), "w", "utf-8") as fp:
                fp.write("\n".join(info))

        # make page, the same as post
        for name, info in post_dict.items():
            with codecs.open('c:\\panda\\src\\page\\{}'.format(name), "w", "utf-8") as fp:
                fp.write("\n".join(info))

        # make template, simple template test cases
        for template_name in ['post', 'page', 'tag', 'month', 'author', 'index', 'category']:
            with codecs.open('c:\\panda\\src\\theme\\default\\{}.html'.format(template_name), "w", "utf-8") as fp:
                fp.write("<h1>hello world</h1>")

    def tearDown(self):
        pass

    pass
